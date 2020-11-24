import socket
from threading import Thread
import os

# STYLING MODULE
from colorama import Fore
from colorama import Style

# GET NICKNAME FROM USER
nickname = input('input nickname: ')

#INITIALISING SOCKET
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = input("server's ip: ")
port = 3000

s.connect((ip, port))

# HANDLING THE RECEPTION OF MESSAGES FROM THE SERVER
def receive():
    while True:
        try:
            smessage = s.recv(1024).decode('ascii')

            if (smessage == 'NICK'): # RESPONDING WITH THE NICKNAME SPECIFIED
                s.send(nickname.encode('ascii'))
            else:
                if nickname in smessage: 
                    # DISPLAY MY MESSAGE IN GREEN
                    print(f'>{Fore.GREEN}{smessage}{Style.RESET_ALL}')
                else:
                    # DISPLAY OTHERS' MESSAGES IN RED
                    print(f'>{Fore.RED}{smessage}{Style.RESET_ALL}')

                
        except:
            print('DISCONNECTED')
            s.close()
            break

# HANDLING THE TRANSMITION OF MESSAGES TO THE SERVER
def send():
    while True:
        message = input()
        print("\033[A                             \033[A") # CLEAR DUPLICATED MESSAGE LINE ABOVE
        s.send(f'({nickname}): {str(message)}'.encode('ascii')) # (John): Hello world!

# STARTING PROCESSES 
Thread(target=receive).start()
Thread(target=send).start()

