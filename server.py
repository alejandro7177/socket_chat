# server.py

import socket
import threading

HOST = '0.0.0.0'
PORT = 12345

clients = []
client_ids = {}
user_id_counter = 0

def broadcast(message, source_client):
    """Función para enviar mensajes a todos los clientes excepto al remitente."""
    for client in clients:
        if client != source_client:
            try:
                client.sendall(message)
            except:
                client.close()
                clients.remove(client)
                client_ids.pop(client, None)

def handle_client(client):
    """Maneja la comunicación con un cliente específico."""
    while True:
        try:
            message = client.recv(1024)
            if message:
                broadcast(message, client)
            else:
                client.close()
                clients.remove(client)
                client_ids.pop(client, None)
                break
        except:
            client.close()
            clients.remove(client)
            client_ids.pop(client, None)
            break

def receive_connections():
    """Acepta nuevas conexiones y crea un hilo para cada cliente."""
    global user_id_counter
    server.listen()
    print(f"Servidor escuchando en {HOST}:{PORT}")
    while True:
        client, address = server.accept()
        print(f"Conectado con {address}")

        client_id = user_id_counter
        user_id_counter += 1
        client_ids[client] = client_id

        client.sendall(f"ID:{client_id}".encode('utf-8'))

        clients.append(client)
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))

    print("Iniciando el servidor...")
    receive_connections()
