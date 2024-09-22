using System;
using System.Net.Sockets;
using System.Text;
using System.Threading;

namespace ChatClient
{
    class Client
    {
        static TcpClient clientSocket = new TcpClient();
        static NetworkStream stream = default(NetworkStream);
        static string clientId = "";
        static string clientName = "";
        static bool isConnected = false;

        static void Main(string[] args)
        {
            Console.Write("Ingresa tu nombre de usuario: ");
            clientName = Console.ReadLine();

            try
            {
                clientSocket.Connect("127.0.0.1", 12345);
                stream = clientSocket.GetStream();
                isConnected = true;

                Thread ctThread = new Thread(GetMessage);
                ctThread.Start();

                while (isConnected)
                {
                    string message = Console.ReadLine();
                    if (!string.IsNullOrEmpty(message))
                    {
                        string fullMessage = $"{clientId}||{clientName}||{message}";
                        byte[] outStream = Encoding.UTF8.GetBytes(fullMessage);
                        stream.Write(outStream, 0, outStream.Length);
                        stream.Flush();
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error al conectar con el servidor: " + ex.Message);
            }
            finally
            {
                if (clientSocket != null && clientSocket.Connected)
                {
                    clientSocket.Close();
                }
            }
        }

        static void GetMessage()
        {
            try
            {
                byte[] bytesFrom = new byte[1024];
                string dataFromServer = "";

                while (isConnected)
                {
                    int bytesRead = stream.Read(bytesFrom, 0, bytesFrom.Length);
                    if (bytesRead > 0)
                    {
                        dataFromServer = Encoding.UTF8.GetString(bytesFrom, 0, bytesRead);

                        if (dataFromServer.StartsWith("ID:"))
                        {
                            clientId = dataFromServer.Substring(3);
                            Console.WriteLine("Tu ID es: " + clientId);

                            string nameMessage = "NAME:" + clientName;
                            byte[] nameBytes = Encoding.UTF8.GetBytes(nameMessage);
                            stream.Write(nameBytes, 0, nameBytes.Length);
                            stream.Flush();
                        }
                        else if (dataFromServer.StartsWith("USERS:"))
                        {
                            Console.WriteLine("Usuarios Conectados:");
                            string usersData = dataFromServer.Substring(6);
                            string[] users = usersData.Split(new string[] { "&&" }, StringSplitOptions.RemoveEmptyEntries);
                            foreach (string user in users)
                            {
                                string[] userInfo = user.Split(new string[] { "||" }, StringSplitOptions.None);
                                if (userInfo.Length == 2)
                                {
                                    string uid = userInfo[0];
                                    string uname = userInfo[1];
                                    Console.WriteLine("ID: {0}, Nombre: {1}", uid, uname);
                                }
                            }
                        }
                        else
                        {
                            Console.WriteLine(dataFromServer);
                        }
                    }
                    else
                    {
                        Console.WriteLine("El servidor ha cerrado la conexión.");
                        isConnected = false;
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error al recibir datos: " + ex.Message);
                isConnected = false;
            }
        }
    }
}
