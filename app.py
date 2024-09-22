import random
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
            chat_client.client_name = st.session_state.username
            chat_client.connect_to_server()
    else:
        # Mostrar el ID asignado y el nombre de usuario
        if chat_client.client_id is not None:
            st.write(f"Tu ID de usuario es: {chat_client.client_id}")
            st.write(f"Tu nombre de usuario es: {chat_client.client_name}")

        # Mostrar la lista de usuarios conectados
        st.subheader("Usuarios Conectados:")
        for uid, uname in chat_client.connected_users:
            st.write(f"ID: {uid}, Nombre: {uname}")

        # Mostrar los mensajes recibidos
        st.subheader("Mensajes:")

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
                # Mensajes propios
                mensaje(
                    message=f"{sender_name}: {content}",
                    is_user=True,
                    avatar_style="lorelei"
                )
            else:
                mensaje(
                    message=f"{sender_name}: {content}",
                    is_user=False,
                    avatar_style="bottts"
                )

        # Campo para ingresar y enviar mensajes dentro de un formulario
        with st.form(key='message_form', clear_on_submit=True):
            message = st.text_input("Escribe tu mensaje", key="message_input")
            submit_button = st.form_submit_button(label='Enviar')

            if submit_button and message:
                # Incluir el ID, nombre y mensaje en el mensaje
                full_message = f"{chat_client.client_id}||{chat_client.client_name}||{message}"
                chat_client.send_message(full_message)
                chat_client.messages.append(full_message)

if __name__ == "__main__":
    main()