from socket import *
import threading
import mysql.connector
import json

class ZchatDB:
    def __init__(self) -> None:

        self.connect = mysql.connector.connect(host='maple.db.ashhost.in', user='u946_VhqYu6cZi0', passwd='d=a^xJuOm4jORFz^Odi!1tm7',database="s946_zchat")
        self.cur = self.connect.cursor()

    def create_user(self):
        pass

    def add_message(self):
        pass
    
db=ZchatDB()

class server:
    def __init__(self) -> None:
        server = socket(AF_INET, SOCK_STREAM)
        server.bind((gethostbyname(gethostname()), 5555))
        server.listen()

        print("Server is listening for incoming connections...")

        self.clients = []

        while True:
            client_socket, client_addr = server.accept()
            print(f"Accepted connection from {client_addr}")
            print(client_addr,client_socket)

            self.clients.append(client_socket)

            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

    def handle_client(self,client_socket:socket):
        while True:
            try:
                # Receive data from the client
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break

                # Broadcast the received message to all connected clients
                self.broadcast(data)

            except Exception as e:
                print(f"Error: {e}")
                break
        
        # Remove the disconnected client
        self.clients.remove(client_socket)
        client_socket.close()

    def process_data(self,client_socket:socket,data):
        try:
            dict_data=json.load(data)
        except:
            client_socket.send()

    def broadcast(self,message):
        for client in self.clients:
            try:
                # Send the message to all connected clients
                client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error: {e}")
                client.close()
                self.clients.remove(client)


server()