from gnuradio import digital
import random 
import numpy 

#configuration parameters 
	#ofdm modulation
""" Here the user can change the relevant parameters of the system""" 
BITS_PER_SYMBOL = 2
FFT_LENGTH      = 16
CP_LENGTH       = 10
FRAME_LENGTH    = 4
BYTES_PER_FRAME = 4
NB_DATA_SYMBOLS = 2

DATA_TONES      = [-5,-4,-2,-1,1,2,4,5]#[-10,-9,-8,-7,-5,-4,-3,-1,1,3,4,5,7,8,9,10]
PILOT_TONES     = [-3,3]#[-11,-6,-2,11,6,2]



#local variables 
"""Here the local variables used to calculate the necessary information are listed"""
map = {
	1:digital.constellation_bpsk(),
	2:digital.constellation_qpsk(),
	3:digital.constellation_8psk()
}

SYNC_SEED = 42

#local functions 
"""internal methods to calculate the information"""
def _mapper_bpsk(number):
	if number == 1:
		return 1
	else:
		return -1
def _mapper_qpsk(number):
	if number == 0:
		return -1j
	elif number == 1:
		return 1
	elif number == 2:
		return 1j
	else:
		return -1

def _get_active_tones():
	active = list()
	for tone in DATA_TONES + PILOT_TONES:
		if tone < 0:
			active.append(tone + FFT_LENGTH)
		else: 
			active.append(tone)
	active.sort() 
	return active	
def _calculate_frame_size():
	size = get_fft_length() + get_cp_length()
def _generate_sync_word_one():
	random.seed(SYNC_SEED)
	active_tones = _get_active_tones()
	sw1 = [numpy.sqrt(4)*_mapper_bpsk(random.getrandbits(1)) if x%2 == 1 and x in active_tones else 0 for x in range(FFT_LENGTH)]
	print(sw1)
	return numpy.fft.fftshift(sw1)
def _generate_sync_word_two():
	random.seed(SYNC_SEED)
	active_tones = _get_active_tones()
	sw2 = [_mapper_bpsk(random.getrandbits(1)) if x in active_tones else 0 for x in range(FFT_LENGTH)]
	print(sw2) 
	sw2[0] = 0j
	return numpy.fft.fftshift(sw2)
#local cache
SYNC_ONE =  _generate_sync_word_one()
SYNC_TWO =  _generate_sync_word_two()
 
#global  functions 
"""methods the users can use to access the relevant parameters"""
def get_constellation():
	return map[BITS_PER_SYMBOL]
def get_bits_per_symbol():
	return BITS_PER_SYMBOL
def get_number_of_data_symbols():
        return NB_DATA_SYMBOLS
def get_fft_length():
	return FFT_LENGTH
def get_cp_length():
	return CP_LENGTH
def get_preambles():
	return [SYNC_ONE,SYNC_TWO]
def get_sync_word_one():
        return SYNC_ONE
def get_sync_word_two():
        return SYNC_TWO
def get_pilot_symbols():
	return [[1,-1]]#[[1,-1,-1,1,1,-1]]
def get_data_tones():
	return [DATA_TONES]
def get_pilot_tones():
	return [PILOT_TONES]
def get_ofdm_frame_length():
	return _calculate_frame_size()
def get_frame_length():
	return FRAME_LENGTH
def get_bytes_per_frame():
        return BYTES_PER_FRAME
	
