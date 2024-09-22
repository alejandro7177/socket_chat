# server.py

import socket
import threading

HOST = 'localhost'
PORT = 12345

clients = []
client_info = {}  # Mapea socket del cliente a (client_id, client_name)
user_id_counter = 0

def broadcast(message, source_client=None):
    """Función para enviar mensajes a todos los clientes excepto al remitente."""
    for client in clients:
        if client != source_client:
            try:
                client.sendall(message.encode('utf-8'))
            except:
                client.close()
                clients.remove(client)
                client_info.pop(client, None)
                send_user_list()

def send_user_list():
    """Envía la lista de usuarios conectados a todos los clientes."""
    user_list = []
    for client, (client_id, client_name) in client_info.items():
        user_list.append(f"{client_id}||{client_name}")
    user_list_message = "USERS:" + "&&".join(user_list)
    for client in clients:
        try:
            client.sendall(user_list_message.encode('utf-8'))
        except:
            client.close()
            clients.remove(client)
            client_info.pop(client, None)

def handle_client(client):
    """Maneja la comunicación con un cliente específico."""
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                if message.startswith("NAME:"):
                    # Recibir el nombre del cliente
                    client_name = message[5:]
                    client_id = client_info[client][0]
                    client_info[client] = (client_id, client_name)
                    print(f"Cliente {client_id} estableció su nombre a {client_name}")
                    send_user_list()
                else:
                    broadcast(message, client)
            else:
                # Mensaje vacío indica desconexión
                client.close()
                clients.remove(client)
                client_info.pop(client, None)
                send_user_list()
                break
        except:
            client.close()
            clients.remove(client)
            client_info.pop(client, None)
            send_user_list()
            break

def receive_connections():
    """Acepta nuevas conexiones y crea un hilo para cada cliente."""
    global user_id_counter
    server.listen()
    print(f"Servidor escuchando en {HOST}:{PORT}")
    while True:
        client, address = server.accept()
        print(f"Conectado con {address}")

        # Asignar un ID único al cliente
        client_id = user_id_counter
        user_id_counter += 1
        client_info[client] = (client_id, "")  # El nombre se establecerá después

        # Enviar el ID al cliente
        client.sendall(f"ID:{client_id}".encode('utf-8'))

        clients.append(client)
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

# Configuración del servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

print("Iniciando el servidor...")
receive_connections()
