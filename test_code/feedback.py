import socket
import time

interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
interface.bind(('192.168.0.2', 9992))
addr = ("192.168.0.2", 9993)
while True:
	recv, addr = interface.recvfrom(1024)
	recv = list(recv)
	print(recv)   
