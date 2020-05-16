import socket
import time

interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
interface.bind(('192.168.0.1', 9991))
addr = ("192.168.0.1", 9990)

msg = bytes([4,4,4,4])
#interface.sendto(msg, addr)
r = []
#for i in range(400):
while True:
	recv, addr = interface.recvfrom(1024)
	recv = list(recv)
	r.append(recv[0])
	print(r)
print(r)


