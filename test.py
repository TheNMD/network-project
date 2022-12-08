import socket, time

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

while True:
    data = 'test'.encode()
    s.sendto(data, ('255.255.255.255', 5002))
    time.sleep(1)