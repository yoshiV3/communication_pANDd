import socket
import time

interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
interface.bind(('192.168.0.2', 9990))
addr = ("192.168.0.2", 9991)
testing = True 
msg = bytes([4,4,4,4]*50)
for i in range(20):
	interface.sendto(msg, addr)
	time.sleep(1)

