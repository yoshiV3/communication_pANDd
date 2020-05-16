import socket
import time

interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
interface.bind(('192.168.0.2', 9991))
addr = ("192.168.0.2", 9990)

msg = bytes([4,4,4,4])
for i in range(4)
	recv, addr = interface.recvfrom(1024)
	recv = list(recv)
	r.append(recv[0])
interface.sendto(msg, addr)
r = []
print(r)

