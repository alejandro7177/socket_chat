#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>     // Para close()
#include <arpa/inet.h>  // Para sockaddr_in, inet_addr()
#include <pthread.h>

#define BUFFER_SIZE 1024

char client_id[10];     // ID asignado por el servidor
char client_name[50];   // Nombre de usuario
int sockfd;             // Descriptor de socket

void *receive_messages(void *arg) {
    char buffer[BUFFER_SIZE];

    while (1) {
        int receive = recv(sockfd, buffer, BUFFER_SIZE, 0);
        if (receive > 0) {
            buffer[receive] = '\0';

            // Procesar mensajes especiales
            if (strncmp(buffer, "ID:", 3) == 0) {
                // Recibir el ID asignado por el servidor
                strcpy(client_id, buffer + 3);
                printf("Tu ID es: %s\n", client_id);

                // Enviar el nombre de usuario al servidor
                char name_message[BUFFER_SIZE];
                sprintf(name_message, "NAME:%s", client_name);
                send(sockfd, name_message, strlen(name_message), 0);
            } else if (strncmp(buffer, "USERS:", 6) == 0) {
                // Recibir la lista de usuarios conectados
                printf("Usuarios Conectados:\n");
                char *users_data = buffer + 6;
                char *token = strtok(users_data, "&&");
                while (token != NULL) {
                    char uid[10], uname[50];
                    sscanf(token, "%[^|]||%s", uid, uname);
                    printf("ID: %s, Nombre: %s\n", uid, uname);
                    token = strtok(NULL, "&&");
                }
            } else {
                // Mensajes normales
                printf("%s\n", buffer);
            }
        } else if (receive == 0) {
            // El servidor cerró la conexión
            printf("Desconectado del servidor.\n");
            exit(0);
        } else {
            perror("Error al recibir datos");
        }
    }
    return NULL;
}

int main() {
    struct sockaddr_in server_addr;

    // Configuración del socket
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1) {
        perror("Error al crear el socket");
        exit(EXIT_FAILURE);
    }

    // Configuración del servidor
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(12345);  // Debe coincidir con el puerto en server.py
    server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");  // Debe coincidir con el host en server.py

    // Conectar al servidor
    if (connect(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) == -1) {
        perror("Error al conectar al servidor");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    // Obtener el nombre de usuario
    printf("Ingresa tu nombre de usuario: ");
    fgets(client_name, 50, stdin);
    client_name[strcspn(client_name, "\n")] = '\0';  // Eliminar el salto de línea

    // Crear un hilo para recibir mensajes
    pthread_t recv_thread;
    if (pthread_create(&recv_thread, NULL, receive_messages, NULL) != 0) {
        perror("Error al crear el hilo de recepción");
        close(sockfd);
        exit(EXIT_FAILURE);
    }

    // Bucle para enviar mensajes
    while (1) {
        char message[BUFFER_SIZE];
        fgets(message, BUFFER_SIZE, stdin);
        message[strcspn(message, "\n")] = '\0';  // Eliminar el salto de línea

        if (strlen(message) == 0) {
            continue;
        }

        // Formatear el mensaje para incluir el ID y el nombre de usuario
        char full_message[BUFFER_SIZE];
        sprintf(full_message, "%s||%s||%s", client_id, client_name, message);

        // Enviar el mensaje al servidor
        if (send(sockfd, full_message, strlen(full_message), 0) == -1) {
            perror("Error al enviar el mensaje");
            break;
        }
    }

    // Cerrar el socket
    close(sockfd);
    return 0;
}
