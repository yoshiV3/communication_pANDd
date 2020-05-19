import socket
import time

interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
interface.bind(('192.168.0.1', 9996))
addr = ("192.168.0.1", 9990)

for i in range(4):
    msg = bytes([x for x in range(200)])
    interface.sendto(msg, addr)
    time.sleep(2)

