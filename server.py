import socket
import threading
import mysql.connector

class ZchatDB:
    def __init__(self) -> None:

        self.connect = mysql.connector.connect(host='maple.db.ashhost.in', user='u926_wGN7NXcLux', passwd='N!.o0GycJTSTA0Jm3VpU.R1F',database="s926_chathistory")
        self.cur = self.connect.cursor()
        self.create_tables()

    def create_tables(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS users(
                mobile_number INT PRIMARY KEY,
                username VARCHAR(100),
                active_ip VARCHAR(15)
            )''')
    
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS message_histroy(
                timestamp INT,
                mobile_number INT,
                message VARCHAR(255)
            )''')
    
    def insert(self,data_list):
        Game_ID = data_list[0]
        Game_Name = data_list[1]
        Category = data_list[2]
        Price = data_list[3]
        Discounted_Price = data_list[4]
        Rating = data_list[5]
        Friends_List = data_list[6]
        Player_Support = data_list[7]

        insert_query = '''
            INSERT INTO Games 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        '''
        data = (Game_ID, Game_Name, Category, Price, Discounted_Price, Rating, Friends_List, Player_Support)
        try:
            self.cur.execute(insert_query, data)
        except:
            self.__init__()
            self.insert()
        self.connect.commit()  

db=ZchatDB()

def handle_client(client_socket):
    while True:
        try:
            # Receive data from the client
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            # Broadcast the received message to all connected clients
            broadcast(data)

        except Exception as e:
            print(f"Error: {e}")
            break

    # Remove the disconnected client
    clients.remove(client_socket)
    client_socket.close()

def broadcast(message):
    for client in clients:
        try:
            # Send the message to all connected clients
            client.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Error: {e}")
            client.close()
            clients.remove(client)

# Set up the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostbyname(socket.gethostname()), 5555))
server.listen()

print("Server is listening for incoming connections...")

clients = []

while True:
    client_socket, client_addr = server.accept()
    print(f"Accepted connection from {client_addr}")
    print(client_addr,client_socket)

    clients.append(client_socket)

    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
