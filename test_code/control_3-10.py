import socket
import time

interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
interface.bind(('192.168.0.2', 9991))
addr = ("192.168.0.2", 9990)

msg = bytes([200]*200)
r = []
recv, addr = interface.recvfrom(4096)
recv = list(recv)
r.append(recv[0])
interface.sendto(msg, addr)
print(r)

