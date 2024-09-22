import socket
import threading

HOST = 'localhost'
PORT = 12345

client_socket = None
messages = []
client_id = None
client_name = None

def receive_messages():
    """Hilo para recibir mensajes del servidor."""
    global client_socket
    global client_id
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                if message.startswith("ID:"):
                    client_id = message[3:]
                    print(f"Tu ID es: {client_id}")
                else:
                    messages.append(message)
            else:
                break
        except:
            break

def connect_to_server():
    """Conecta al cliente con el servidor y comienza el hilo de recepción."""
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    threading.Thread(target=receive_messages, daemon=True).start()

def send_message(message):
    """Envía un mensaje al servidor."""
    global client_socket
    if client_socket:
        client_socket.sendall(message.encode('utf-8'))
