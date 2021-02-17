#!/usr/bin/env python3

import socket
from config import IP_ADDRESS, PORT


class PeerServer:
    def __init__(self):
        self.host = "127.0.0.1"  # IP_ADDRESS
        self.port = PORT

    def run(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(5)
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                print(data)
                conn.send(b"[Server] data")
            conn.close()


server = PeerServer()
server.run()
