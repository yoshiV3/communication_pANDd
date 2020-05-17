import socket
import time

interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
interface.bind(('192.168.0.2', 9991))
addr = ("192.168.0.2", 9990)
msg = bytes([200]*200)
#recv, r = interface.recvfrom(4096)
#recv = list(recv)
interface.sendto(msg, addr)
#print(recv)

