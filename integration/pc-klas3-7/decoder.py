from basic_operations import *
def syndromes(msg):
	synd     = [0,0]
	eval_sum = msg[0] ^ msg[1] ^ msg[2] ^ msg[3]
	synd[1]  = eval_sum
	eval_sum = mul(msg[0],8) ^ mul(msg[1],4) ^ mul(msg[2],2) ^ msg[3]
	synd[0]  = eval_sum
	return synd 
def location(synd):
	return 3-discrete_log(mul(synd[0], inverse(synd[1])))
def correct_msg(msg, synd , pos):
        magnitude = synd[1]#mul(omega[0],loc_inv) ^ omega[1]#mul(omega[0],pw(loc_inv, 2)) ^ mul(omega[1],loc_inv) ^ omega[2]
        msg[pos]  = msg[pos] ^ magnitude
        return msg 
def decoder(inputm):
	msg = inputm.copy()
	synd = syndromes(msg)
	if (synd[0] == synd[1] == 0):
		return msg
	if (synd[0] == 0 or synd[1] == 0):
		return [msg[0], msg[1]]
	loc  = location(synd)
	if loc < 0:
		return [msg[0], msg[1]]
	return correct_msg(msg, synd, loc)
