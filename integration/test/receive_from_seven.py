import socket
import time

interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
interface.bind(('192.168.0.2', 9993))

err     = 0
counter = 0
for i in range(800):
    recv, r = interface.recvfrom(1024)
    recv = list(recv)[0]
    counter = counter + 1
    if recv != 4:
        err = err + 1
    print("Received: " + str(counter) + " (number of errors:" + str(err)+")" )
  
