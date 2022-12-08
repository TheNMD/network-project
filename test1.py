#udp receive broadcast
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 5002))

while True:
    print(s.recv(1024))