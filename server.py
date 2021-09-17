import socket
import threading

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_connection(client):
    stop = False
    while not stop:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            nickename = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f"{nickname} left the chat".encode('utf-8'))
            stop = True

def main():
    print("Server is running....")
    while True:
        client, addr = server.accept()
        print(f"Connected to {addr}")

        client.send("NICK".encode('utf-8'))

        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print("Nickname is {}".format(nickname))

        broadcast("{} joined!".format(nickname).encode('utf-8'))

        client.send("You are now connected!".encode('utf-8'))

        thread = threading.Thread(target=handle_connection, args=(client,))
        thread.start()

if __name__ == '__main__':
    main()
