import  socket
import  threading

interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
interface.bind(('192.168.0.1', 9991))
testing = True
def receive():
        while testing:
                recv, addr = interface.recvfrom(1024)
                recv = list(recv)
                print(str(recv))
threading.Thread(target=receive).start()




