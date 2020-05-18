from basic_operations import *
def scale_poly(p,x):
	r = [0] * len(p)
	for i in range(0, len(p)):
		r[i] = mul(p[i], x)
	return r
def add_poly(p,q):
	r = [0] * max(len(p),len(q))
	for i in range(0,len(p)):
		r[i+len(r)-len(p)] = p[i]
	for i in range(0,len(q)):
		r[i+len(r)-len(q)] ^= q[i]
	return r
def mul_poly(p,q):
	r = [0] * (len(p)+len(q)-1)
	for j in range(0, len(q)):
		for i in range(0, len(p)):
			r[i+j] ^= mul(p[i], q[j])
	return r		
def eval_poly(poly, x):
	y = poly[0]
	for i in range(1, len(poly)):
		y = mul(y, x) ^ poly[i]
	return y

