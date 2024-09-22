import streamlit as st
from streamlit_chat import message as mensaje
import chat_client
from streamlit_autorefresh import st_autorefresh

st.title("Aplicación de Chat en Tiempo Real")

if 'username' not in st.session_state:
    st.session_state.username = ''

def main():
    st_autorefresh(interval=2000, key="chat_refresh")

    if not st.session_state.username:
        st.session_state.username = st.text_input("Ingresa tu nombre de usuario")
        if st.session_state.username:
            chat_client.connect_to_server()
            chat_client.client_name = st.session_state.username
    else:
        # Mostrar el ID asignado y el nombre de usuario
        if chat_client.client_id is not None:
            st.write(f"Tu ID de usuario es: {chat_client.client_id}")
            st.write(f"Tu nombre de usuario es: {chat_client.client_name}")

        st.subheader("Mensajes:")
        AvatarStyle = [
            "adventurer",
            "adventurer-neutral",
            "avataaars",
            "avataaars-neutral",
            "big-ears",
            "big-ears-neutral",
            "big-smile",
            "bottts",
            "bottts-neutral",
            "croodles",
            "croodles-neutral",
            "fun-emoji",
            "icons",
            "identicon",
            "initials",
            "lorelei",
            "lorelei-neutral",
            "micah",
            "miniavs",
            "open-peeps",
            "personas",
            "pixel-art",
            "pixel-art-neutral",
            "shapes",
            "thumbs",
        ]

        for msg in chat_client.messages:
            # Analizar el mensaje para extraer ID, nombre y contenido
            parts = msg.split("||")
            if len(parts) == 3:
                sender_id, sender_name, content = parts
            elif len(parts) == 2:
                sender_id, content = parts
                sender_name = "Desconocido"
            else:
                sender_id = "Desconocido"
                sender_name = "Desconocido"
                content = msg

            if sender_id == chat_client.client_id:
                mensaje(
                    message=f"{sender_name}: {content}",
                    is_user=True,
                    avatar_style=AvatarStyle[15]
                )
            else:
                mensaje(
                    message=f"{sender_name}: {content}",
                    is_user=False,
                    avatar_style=AvatarStyle[2]
                )

        with st.form(key='message_form', clear_on_submit=True):
            message = st.text_input("Escribe tu mensaje", key="message_input")
            submit_button = st.form_submit_button(label='Enviar')

            if submit_button and message:
                full_message = f"{chat_client.client_id}||{chat_client.client_name}||{message}"
                chat_client.send_message(full_message)
                chat_client.messages.append(full_message)

if __name__ == "__main__":
    main()
