#!/usr/bin/env python3
import socket
import os
import subprocess

def main():

    #Setup network parameters and create socket.
    localhost = '127.0.0.1'
    PORT = 9001
    BUF = 20 #Small response

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((localhost, PORT))

    while True:
        s.listen(1)
        conn, addr = s.accept()
        print('Connection from: ' + str(addr))
        parameters = conn.recv(BUF)
        print("Parameters received: " + str(parameters.decode('utf-8')))
        print("Starting C program...")
        result = subprocess.run("./dummy", stdout=subprocess.PIPE)
        #print(result.<stdout/stderr>) to see response or error.


if __name__ == '__main__':
    main()
