import socket
from threading import Thread

# INITIALISING SOCKET
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = input('open port (default is 3000): ')

if (port):
    server.bind(('0.0.0.0', int(port)))
else:
    server.bind(('0.0.0.0', 3000))

server.listen(2)

# INITIALISING LISTS OF CLIENTS AND NICKNAMES FOR MONITORING
clients = []
nicknames = []

# BROADCAST MESSAGE TO CLIENTS


def broadcast(message):
    for client in clients:
        client.send(message)

# HANDLING CLIENT AND KICKING IN CASE OF INACTIVITY


def handle_client(client):
    while True:
        try:
            index = clients.index(client)
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

# HANDLING THE RECEPTION OF MESSAGES FROM DIFFERENT CLIENTS


def receive():
    while True:
        client, adress = server.accept()
        print(f'connected {adress}')  # server-side log message

        # GETTING NICKNAME
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')

        # ADDING CLIENT TO LISTS
        nicknames.append(nickname)
        clients.append(client)

        print(f'{nickname} connected')  # server-side log message
        broadcast(f'{nickname} joined the chat'.encode(
            'ascii'))  # global message

        # ASIGNING A NEW THREAD TO EVERY NEW CLIENT
        thread = Thread(target=handle_client, args=(client,))
        thread.start()


print('Server is running and listening...')
receive()
