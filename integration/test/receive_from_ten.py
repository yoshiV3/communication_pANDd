import socket
import time

interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
interface.bind(('192.168.0.1', 9991))

err     = 0
counter = 0
for i in range(4):
    recv, r = interface.recvfrom(1024)
    recv = list(recv)
    print(recv)
    err = 0
    for index in range(len(recv)):
        if recv[index] != index:
            err = err + 1
    counter = counter + 1
    print("Received: " + str(counter) + " (number of errors:" + str(err)+")" )
