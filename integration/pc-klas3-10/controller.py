import socket 
import threading 
import buffer
import encoder
import decoder
import time

own_ip       = "192.168.0.2"
own_port_in  = 9990
own_port_out = 9991
own_port_tod = 9992
own_port_frd = 9993
own_port     = 9994
own_port_two = 9995

lock_input      = threading.Lock()
trans_buffer    = buffer.Buffer(5)
output_encoded  = []
gen             = encoder.rs_generator_poly()

def put_data_from_socket_to_buffer():
    global lock_input
    global trans_buffer
    global own_ip
    global own_port_in
    interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    interface.bind((own_ip, own_port_in))
    while True:
        recv_b, addr = interface.recvfrom(1024)
        recv = list(recv_b)
        print('new data')
        stored_data = False 
        while not stored_data:
            if len(recv) == 200:
                with lock_input:                
                    trans_buffer.write(recv)
                    stored_data = True
            else:
                stored_data = True  

def transmit():
    global lock_input
    global updating_buffer
    global gen
    global own_ip
    global own_port
    global own_port_tod
    interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    interface.bind((own_ip, own_port))
    target   = (own_ip,own_port_tod)
    queue  = []
    q      = [0,0,0,0]
    preamble = [x for x in range(12)]
    while True:
        if (trans_buffer.um > 0):
            with lock_input:
                queue = trans_buffer.read().copy()
            msg = bytes(preamble[:4])
            interface.sendto(msg, target)
            msg = bytes(preamble[4:8])
            interface.sendto(msg, target)
            msg = bytes(preamble[8:])
            for index in range(100):
                interface.sendto(msg, target)
                number = queue[index*2]
                low  = number&15
                high = (number&240) >> 4
                out_s_one = encoder.encode_msg([high,low], gen)
                number = queue[index*2+1]
                low2  = number&15
                high2 = (number&240) >> 4
                out_s_two = encoder.encode_msg([high2,low2], gen)       
                q[0] = (high << 4) + high2
                q[1] =  (low << 4) + low2
                q[2] = (out_s_one[2]  << 4) + out_s_two[2]
                q[3] = (out_s_one[3]  << 4) + out_s_two[3]
                msg = bytes(q)
            interface.sendto(msg,target)
            time.sleep(0.05)
            msg = bytes([0,0,0,0])
            interface.sendto(msg, target)
            time.sleep(0.05)
            interface.sendto(msg, target)   
            
def receive():
    global own_ip
    global own_port_frd 
    global output_encoded              
    interface_d  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    interface_d.bind((own_ip, own_port_frd))
    state = 0
    hist  = [0]*12
    intra = []
    pre   = 0
    while True:  
        recv_b, addr = interface_d.recvfrom(1024)
        recv_l = list(recv_b)
        for recv in recv_l:
            if state == 0:
                hist.pop(0)
                hist.append(recv)
                exp = 0
                err = 0 
                for element in hist:
                    err = err + 1 if element != exp else err
                    exp = exp + 1
                if err <= 2:
                    state = 1
                    pre = 0
            elif state == 1:
                intra.append(recv)                              
                pre   = pre + 1
                state = 2 if pre == 399 else 1
            elif state ==2:
                intra.append(recv)
                output_encoded.append(intra.copy())
                intra = []
                state = 0
                hist  = [0]*12   
def send_decoded_data():
    global own_ip
    global own_port_two
    global own_port_out 
    global output_encoded
    output = []    
    r_one  = [0,0,0,0]
    r_two  = [0,0,0,0]  
    interface_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    interface_out.bind((own_ip, own_port_two))
    target = (own_ip,own_port_out)
    msg = [0,0,0,0]
    while True:
        if len(output_encoded)>0:
            print('sending')
            current = output_encoded.pop(0)
            for word in range(100):
                for i in range(4):
                    r_one[i] =  (current[word*4+i]&240) >> 4
                    r_two[i] =  (current[word*4+i]&15)
                rslt    = decoder.decoder(r_one)
                number  = (rslt[0] << 4) + rslt[1]
                output.append(number)
                rslt    = decoder.decoder(r_two)
                number  = (rslt[0] << 4) + rslt[1]
                output.append(number)
            msg_o = bytes(output)
            interface_out.sendto(msg_o, target)
            output = []            
def main():
    threading.Thread(target=put_data_from_socket_to_buffer).start()
    threading.Thread(target=transmit).start()                                   
    threading.Thread(target=receive).start()                                                  
    threading.Thread(target=send_decoded_data).start()
main()    	               	            
    	         
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
                    
