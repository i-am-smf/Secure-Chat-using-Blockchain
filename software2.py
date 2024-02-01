import socket
import threading

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
server.bind(('172.27.14.222', 5555))
server.listen()

print("Server is listening for incoming connections...")

clients = []

while True:
    client_socket, client_addr = server.accept()
    print(f"Accepted connection from {client_addr}")

    # Add the new client to the list
    clients.append(client_socket)

    # Create a new thread to handle the client
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
