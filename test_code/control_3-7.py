import socket
import time

interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
interface.bind(('192.168.0.1', 9991))
addr = ("192.168.0.1", 9990)

for i in range(1):
    msg = bytes([200]*200)
    #interface.sendto(msg, addr)
    recv, r = interface.recvfrom(1024)
    recv = list(recv)
    err = 0
    print(len(recv))
    for element in recv:
        if element != 200:
           err = err + 1
    print("number of errors:" + str(err) )
    print(recv)

