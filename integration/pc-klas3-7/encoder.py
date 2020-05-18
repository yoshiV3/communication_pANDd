from basic_operations import *
from poly_operations  import *
 
def rs_generator_poly():
	g = [1]
	for i in range(0, 2):
		g = mul_poly(g, [1, pw(2, i)])
	return g

def encode_msg(msg, gen):
	msg_out = [0] * (4)
	msg_out[:2] = msg
	for i in range(2):
	 	coef = msg_out[i]
	 	if coef != 0:
	 		for j in range(1, 3):
	 			msg_out[i+j] ^= mul(gen[j], coef)
	msg_out[:2] = msg
	return msg_out	

