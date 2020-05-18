print('basic_operations is beening imported, generating basic variables')
__table_exp__            = [0]*32
__table_log__            = [0]*16
exp = 1
for i in range(15):
	__table_exp__[i]     = exp
	__table_exp__[i+15]  = exp
	__table_log__[exp]   = i
	exp = exp<<1
	if exp & 0x10:
		exp ^= 19
__table_exp__[31] = __table_exp__[16]
__table_exp__[30] = __table_exp__[15]

def mul(x,y):
	if x == 0 or y == 0:
		return 0
	else :
		return __table_exp__[__table_log__[x] + __table_log__[y]]
def pw(x, pow):
	return __table_exp__[(__table_log__[x]*pow)%255]
def inverse(x):
    	return __table_exp__[15 - __table_log__[x]] 
def discrete_log(x):
	return __table_log__[x]
