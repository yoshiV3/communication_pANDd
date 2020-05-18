import socket
import time

interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
interface.bind(('192.168.0.1', 9991))
addr = ("192.168.0.1", 9992)

for i in range(200):
    msg = bytes([4,4,4,4])
    interface.sendto(msg, addr)
    time.sleep(0.1)

