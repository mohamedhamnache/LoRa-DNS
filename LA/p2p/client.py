import socket


class PeerClient:
    def __init__(self):
        pass


"""
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    data = s.recv(1024)
    s.sendall(b'Hello from LoRaWAN Roaming')
print('Received', repr(data))
"""
