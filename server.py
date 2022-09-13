import socket
import threading

host = "127.0.0.1"
port = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = (client.recv(1024))
            print(f"{nicknames[clients.index(client)]}: {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected at {str(address)}.\n")

        nickname = (client.recv(1024)).decode("utf-8")

        nicknames.append(nickname)
        clients.append(client)

        print(f"{nickname} connected.\n")
        broadcast(f"{nickname} has joined the chat.\n".encode("utf-8"))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server Online.\nYou can now open client.")
receive()