# chat_client.py

import socket
import threading

HOST = 'localhost'
PORT = 12345

client_socket = None
messages = []
client_id = None  # ID asignado por el servidor
client_name = None  # Nombre de usuario
connected_users = []  # Lista de usuarios conectados

def receive_messages():
    """Hilo para recibir mensajes del servidor."""
    global client_socket
    global client_id
    global connected_users
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                if message.startswith("ID:"):
                    # Recibir el ID asignado por el servidor
                    client_id = message[3:]
                    print(f"Tu ID es: {client_id}")
                    # Enviar el nombre de usuario al servidor
                    client_socket.sendall(f"NAME:{client_name}".encode('utf-8'))
                elif message.startswith("USERS:"):
                    # Recibir la lista de usuarios conectados
                    users_data = message[6:].split("&&")
                    connected_users.clear()
                    for user_data in users_data:
                        if user_data:
                            uid, uname = user_data.split("||")
                            connected_users.append((uid, uname))
                else:
                    messages.append(message)
            else:
                break
        except Exception as e:
            print(f"Error al recibir mensajes: {e}")
            break

def connect_to_server():
    """Conecta al cliente con el servidor y comienza el hilo de recepción."""
    global client_socket
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        threading.Thread(target=receive_messages, daemon=True).start()
    except Exception as e:
        print(f"Error al conectar al servidor: {e}")

def send_message(message):
    """Envía un mensaje al servidor."""
    global client_socket
    if client_socket:
        try:
            client_socket.sendall(message.encode('utf-8'))
        except Exception as e:
            print(f"Error al enviar mensaje: {e}")
