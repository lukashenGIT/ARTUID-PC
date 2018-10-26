#!/usr/bin/env python3
import socket

def main():
    TCP_IP = '127.0.0.1'
    PORT = 9001
    BUF = 20 #Small response

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, PORT))

    while True:
        s.listen(1)
        conn, addr = s.accept()
        print('Connection from: ' + str(addr))
        parameters = conn.recv(BUF)
        print("Parameters: " + str(parameters.decode('utf-8')))


if __name__ == '__main__':
    main()
