import  socket
import  threading

interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
interface.bind(('192.168.0.1', 9991))
testing = True
def receive():
        number    =  0
        incorrect = 0
        while testing:
                number = number + 1
                recv, addr = interface.recvfrom(1024)
                recv = list(recv)
                if recv[0] != 4:
                   incorrect = incorrect + 1
                print(str(number) +": " + str(recv)+" ("+str(incorrect)+")")
threading.Thread(target=receive).start()




