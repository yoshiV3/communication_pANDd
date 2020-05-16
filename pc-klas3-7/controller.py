import socket 
import threading 
import buffer

own_ip       = "192.168.0.1"
target_ip    = "192.168.0.1"
own_port_in  = 9990
own_port_out = 9991
own_port_tod = 9992
own_port_frd = 9993
own_port     = 9994
own_port_two = 9995


queue_trans          = []
queue_ack            = []
queue_retr           = []
queue_main           = []
qtrns                = False
qretr                = False
qack                 = False
updating_buffer      = False 
trans_buffer         = buffer.Buffer(5) 
currect_packet       = []
r_buf                = []
t_buf                = []
a_buf                = []
ab                   = False 
rb                   = False
tb                   = False  
output               = []
outp                 = False 
temp_pack            = []
tmppa                = False 

def retrieve_data():
	global queue_trans
	global queue_main
	global qtrns
	global updating_buffer
	global current_packet 
	global trans_buffer
	while True:
	    can_transmit=   (not updating_buffer) and ( not qtrns) and (trans_buffer.um > 0)  #There is new data, there is no transmission and the buffer is not being updated
	    if can_transmit:
	        updating_buffer = True
	        current_packet = trans_buffer.read().copy()
	        queue_trans.append(current_packet.copy())
	        updating_buffer = False
	        qtrns = True
	        queue_main.append(0)
def put_data_from_socket_to_buffer():
    global updating_buffer
    global trans_buffer
    global own_ip
    global own_port_in
    interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    interface.bind((own_ip, own_port_in))
    while True:
        recv_b, addr = interface.recvfrom(1024)
        recv = list(recv_b)
        while updating_buffer:
            pass
        updating_buffer = True
        trans_buffer.write(recv)
        updating_buffer = False
def transmit():
    global queue_main
    global queue_trans
    global qtrns
    global queue_retr
    global qretr
    global queue_ack
    global qack
    global target_ip
    global own_ip
    global own_port
    global own_port_tod
    interface = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    interface.bind((own_ip, own_port))
    target   = (target_ip,own_port_tod)
    first_packetT = [3 for i in range(25)]
    first_packetA = [5 for i in range(25)]
    first_packetR = [6 for i in range(25)]
    fragment = [0 for x in range(25)]
    while True:
        if len(queue_main) >= 1:
            typ = queue_main.pop(0)
            if typ ==0:
        	    fragment = first_packetT.copy()
        	    queue     = queue_trans.pop(0)
            elif typ ==1:
        	    fragment = first_packetA.copy()
        	    queue     = queue_ack.pop(0)
            else:
        	    fragment = first_packetR.copy()
        	    queue     = queue_retr.pop(0)   
            for i in range(int(len(queue)/20)):
                msg = bytes(fragment)
                interface.sendto(msg, target)
                fragment[:20] = queue[i*20:(i+1)*20].copy()
                fragment[20]  = fragment[0] ^ fragment[5] ^ fragment[10] ^ fragment[15] 
                fragment[21]  = fragment[1] ^ fragment[6] ^ fragment[11] ^ fragment[16] 
                fragment[22]  = fragment[2] ^ fragment[7] ^ fragment[12] ^ fragment[17] 
                fragment[23]  = fragment[3] ^ fragment[8] ^ fragment[13] ^ fragment[18] 
                fragment[24]  = fragment[4] ^ fragment[9] ^ fragment[14] ^ fragment[19]
            interface.sendto(bytes(range(25)),target)
            if typ == 1:
    	        qack = False 
            elif type == 2:
    	        if len(queue_retr) == 0:
    	    	    qretr = False 
    	    	    gtrns = False 
def receive():
    global own_ip
    global own_port_frd
    global r_buf
    global t_buf
    global a_buf
    global rb
    global tb
    global ab
    state = 0
    pre_a = 0
    err_a = 0
    pre_t = 0
    err_t = 0
    pre_r = 0
    err_r = 0
    dre   = False 
    interface_d  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    interface_d.bind((own_ip, own_port_frd))
    while True:
        recv_b, addr = interface_d.recvfrom(1024)
        recv = list(recv_b)
        if state == 0: #drop noise and wait for a transmission
            for r in recv:
                err_a = err_a    if r  == 5 else err_a + 1
                err_r = err_r    if r  == 6 else err_r + 1
                err_t = err_t    if r  == 3 else err_r + 1
                pre_a = pre_a +1 if err_a <= 2 else 0
                pre_r = pre_r +1 if err_r <= 2 else 0
                pre_t = pre_t +1 if err_t <= 2 else 0
                err_a =  0       if err_a >  2 else err_a 
                err_r =  0       if err_r >  2 else err_r
                err_t =  0       if err_t >  2 else err_t  
                state = 3  if (pre_r == 25)    else 0 
                state = 2  if pre_a == 25      else 0 
                state = 1  if pre_t == 25     else 0 
        elif state == 1:
            if tb:
                state = 10
            else:
                pre_t = 5
                for element in recv:
                    t_buf.append(element)
                state  = 4.
        elif state == 4:
            pre_t = pre_t + 5
            for element in recv:
                t_buf.append(element)
            state = 7 if pre_t == 250 else 4
        elif state == 2:
            if ab:
                state = 10
            else:
                for element in recv:
                    a_buf.append(element)
                pre_a = 5
                state = 5 
        elif state == 5:
            pre_a = pre_a + 5
            for element in recv:
                a_buf.append(element)
            state = 8 if pre_a == 25 else 5
        elif state == 3:
            if rb:
                state = 10
            else:
                for element in recv:
                    r_buf.append(element)
                pre_r = 5
                state = 6
        elif state == 6:
            pre_r = pre_r + 5
            for element in recv:
                r_buf.append(element)
            state = 9 if pre_r == 25 else 6
        elif state == 7:
            tb    = True 
            state = 10        
        elif state == 8:
            ab    = True
            state = 10
        elif state ==9:
            rb    = True
            state = 10 
        if state == 10:
            state = 0
            pre_r = 0
            err_r = 0
            pre_t = 0
            err_t = 0
            pre_a = 0
            err_a = 0           	
def send_r_data():
    global own_ip
    global own_port_two
    global own_port_frd
    global own_port_out
    global output
    global outp
    interface_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    interface_out.bind((own_ip, own_port_two))
    target = (own_ip,own_port_out)
    while True:
        if outp:
            msg = bytes(output)
            interface_out.sendto(msg, target)
            output = []
            outp = False 
def parse_recv():
    global tb
    global t_buf
    global temp_pack
    global tmppa
    global queue_main
    global queue_ack
    global qack
    while True:
        if tb:
            if not (qack or tmppa):
                q = [255]*20
                c = 0
                for p in range(10):
                    for i in range(20):
                        temp_pack.append(t_buf[p*25 + i])                
                    correct =             t_buf[p*25+20]  == t_buf[p*25+0] ^ t_buf[p*25+5] ^ t_buf[p*25+10] ^ t_buf[p*25+15] 
                    correct = correct and t_buf[p*25+21]  == t_buf[p*25+1] ^ t_buf[p*25+6] ^ t_buf[p*25+11] ^ t_buf[p*25+16] 
                    correct = correct and t_buf[p*25+22]  == t_buf[p*25+2] ^ t_buf[p*25+7] ^ t_buf[p*25+12] ^ t_buf[p*25+17] 
                    correct = correct and t_buf[p*25+23]  == t_buf[p*25+3] ^ t_buf[p*25+8] ^ t_buf[p*25+13] ^ t_buf[p*25+18] 
                    correct = correct and t_buf[p*25+24]  == t_buf[p*25+4] ^ t_buf[p*25+9] ^ t_buf[p*25+14] ^ t_buf[p*25+19]
                    if correct:
    	                q[10+p] = 255
    	                c = c +1
                    else:
    	                q[10+p] = 0
                if c == 10:
                    for i in range(10):
                        q[i]  = 0
                    output = temp_pack.copy()
                    outp   = True
                queue_ack.append(q)
                tmppa  = True   
                qack   = True
                queue_main.append(1)
                t_buf = []
                tb    = False   	            
def parse_ack():
    global ab
    global a_buf 
    global queue_retr
    global qretr
    global qtrns
    global current_packet
    global queue_main
    while True:
        if ab:
           if not qretr:
               re = []
               z  = 0
               for index in range(10):
                   z = z + 1 if a_buf[index] == 0 else z
               if z > 7:
                   qtrns = False 
               else:
                   final = [10]*20
                   i = 0
                   for p in range(10):
                        if a_buf[p+10] != 255:
                              re = current_packet[p*20:(p+1)*20]
                              final[10+i] = p
                              i           =  i + 1
                              queue_retr.append(re.copy())
                              queue_main.append(2)
                              qretr = True
                   queue_retr.append(final)                                                              
                   queue_main.append(2)
                   qretr = True                                   
               a_buf = []
               ab    = False 
def parse_re():
    global r_buf
    global rb
    global temp_pack
    global tmppa
    intra = []
    while True:
        if rb:
            temp = r_buf.copy()
            rb = False
            if tmppa:
                intra.append(temp)
                z  = 0
                for index in range(10):
                    z = z + 1 if temp[index] == 10 else z
                if z > 8:
                    pre = -1
                    for i in range(len(intra)-1):
                        index =  temp[10+i] 
                        if pre < index < 10:
                            temp_pack[index*20: (index+1)*20] = intra[i][0:20]
                output =  temp_pack.copy()
                outp   = True                                       
def main():
    threading.Thread(target=retrieve_data).start()
    threading.Thread(target=put_data_from_socket_to_buffer).start()                                   
    threading.Thread(target=transmit).start()                                                  
    threading.Thread(target=receive).start()
    threading.Thread(target=send_r_data).start()
    threading.Thread(target=parse_recv).start()
    threading.Thread(target=parse_ack).start()
    threading.Thread(target=parse_re).start()
main()    	               	            
    	            
    	            
    	            
    	            
    	            
    	            
    	            
    	            
    	            
    	            
    	            
    	            
    	            
    	            
    	            
    	            
    	            
    	            
    	            
    	            
    	            
    	            
    	            
    	            
    	            
    	            
    	            
    	            
    	            
    	
