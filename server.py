from socket import *
import threading
import mysql.connector
import json

class ZchatDB:
    def __init__(self) -> None:
        self.connect = mysql.connector.connect(host='maple.db.ashhost.in', user='u946_VhqYu6cZi0', passwd='d=a^xJuOm4jORFz^Odi!1tm7',database="s946_zchat")
        self.cur = self.connect.cursor()
        print("Database connected successfully")

    def add_message(self):
        pass
    
    def check_user(self,mobile_number,active_ip):
        try:
            self.cur.execute(f"SELECT * FROM users where mobile_number = dataenc({mobile_number})")
            result=self.cur.fetchall()
        except:
            return False
        
        if len(result)>0:
            self.cur.execute(f"UPDATE users SET active_ip = '{active_ip}' where mobile_number = '{mobile_number}'")
            self.connect.commit()
            try:
                self.connect.close()
            except:
                pass
            self.__init__()
            return True
        else:
            return False

    def get_username(self,mobile_number):
        self.cur.execute(f"SELECT username FROM users where mobile_number = dataenc({mobile_number})")
        result=self.cur.fetchone()
        if len(result)==1:
            return result[0][0]
        else:
            return "Nick"
        
    def new_user(self,username,mobile_number,active_ip):
        
        insert_query = '''
            INSERT INTO users(username,mobile_number,active_ip) 
            VALUES (%s, %s, %s)
        '''
        print(f"New use created.\nusername: {username}\nMobile Number: {mobile_number}\nActive IP: {active_ip}")
        data = (username,mobile_number,active_ip)

        try:
            self.cur.execute(insert_query, data)

        except:

            self.__init__()
            self.new_user()

        self.connect.commit()
        try:
            self.connect.close()
        except:
            pass
        self.__init__()

        return True

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
                self.process_data(client_socket,data)
            except Exception as e:
                print(f"Error: {e}")
                break
        
        # Remove the disconnected client
        self.clients.remove(client_socket)
        client_socket.close()

    def process_data(self,client_socket:socket,data):
        data_json={}
        try:
            dict_data=json.loads(data)
            if dict_data['process']=="user_check":
                if db.check_user(dict_data['mobile_number'],client_socket.getsockname()[0]):
                    data_json['process']="found"
                    client_socket.send(json.dumps(data_json).encode('utf-8'))
                else:
                    data_json['process']="notfound"
                    client_socket.send(json.dumps(data_json).encode('utf-8'))
                return

            if dict_data['process']=="new_user":
                if db.new_user(dict_data['username'],dict_data['mobile_number'],client_socket.getsockname()[0]):
                    dict_data={
                        "process":"new_user_created",
                        "status":True
                    }
                    client_socket.send(json.dumps(dict_data).encode("utf-8"))
                return
            
            if dict_data['process']=="message_boardcast":
                print(dict_data)
                dict_data['username']=db.get_username(dict_data['mobile_number'])
                self.broadcast(dict_data)
                return
            
        except Exception as e:
            data_json['process']="error"
            client_socket.send(json.dumps(data_json).encode('utf-8'))
            raise e
        
    def broadcast(self,message):
        for client in self.clients:
            try:
                client.send(json.dumps(message).encode('utf-8'))
                print("Sended")
                
            except Exception as e:
                print(f"Error: {e}")
                client.close()
                self.clients.remove(client)


server()