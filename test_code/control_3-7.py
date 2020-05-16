import socket
import time

interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
interface.bind(('192.168.0.1', 9991))
addr = ("192.168.0.1", 9990)

msg = bytes([200]*200)
interface.sendto(msg, addr)
r = []
for i in range(400):
	recv, addr = interface.recvfrom(1024)
	recv = list(recv)
	r.append(recv)
print(r)


