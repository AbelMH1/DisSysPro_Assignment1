import socket
from time import sleep

HOST = 'localhost'
PORT = 64000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    answ = input('You want to consume latest stats? (y/n): ').strip()[0].lower()
    if answ == 'y':
        sock.connect((HOST, PORT))
        sock.sendall('Recivedata'.encode())
        while True:
            data = sock.recv(512).decode()
            if not data:
                break
            print('Received:  ', data)
    else:
        print('Ok, goodbye!')



