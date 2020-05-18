import configuration as config 
from gnuradio import gr, blocks, fft, analog, digital 
import ofdmAux as aux

LEN_TAG_KEY     = 'frame_len'
SCRAMBLED_SEED  =  41
SAFETY          =  0
class Transmitter(gr.hier_block2):
   def __init__(self):
        gr.hier_block2.__init__(self, "ofdm_tx",
					gr.io_signature(1, 1, gr.sizeof_char),
                    			gr.io_signature(1, 1, gr.sizeof_gr_complex))
        self.sequencr = aux.insert_sequence_numbers_bb()
        self.encoderf  = aux.encoder_reed_solomon_bb()                     			
        self.framer   = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, config.get_bytes_per_frame() , LEN_TAG_KEY) #divide the incoming data streams in frames
        self.connect(self, self.sequencr, self.encoderf,self.framer)
                #We can do some byte scrambling if needed (variable modulus modulation ) 		
        self.unpacker_data_stream   = blocks.repack_bits_bb(    #modulation of the data (split the bytes, and modulate the split bytes 
				8,
				config.get_bits_per_symbol(),
				LEN_TAG_KEY
        )
        self.modulator_data_stream   = digital.chunks_to_symbols_bc(config.get_constellation().points())
        self.connect(self.framer, self.unpacker_data_stream,self.modulator_data_stream)
        self.allocator = digital.ofdm_carrier_allocator_cvc(
				    config.get_fft_length(),
				    occupied_carriers=config.get_data_tones(),
				    pilot_carriers   =config.get_pilot_tones(),
				    pilot_symbols    = config.get_pilot_symbols(),
				    sync_words       = config.get_preambles(),
				    len_tag_key      = LEN_TAG_KEY
        )
        self.connect(self.modulator_data_stream, self.allocator)
        self.fft_block      = fft.fft_vcc(
					config.get_fft_length(),
					False, 
					(),
					True
        )
        self.connect(self.allocator,self.fft_block)
        self.prefixer = digital.ofdm_cyclic_prefixer(
				config.get_fft_length(),
				config.get_cp_length() + config.get_fft_length(),
				0,
				LEN_TAG_KEY
			)
        self.burst_handler = aux.add_zeros_cc(1,104)#digital.burst_shaper_cc([],1040,1040,False, LEN_TAG_KEY)
        self.connect(self.fft_block, self.prefixer, self.burst_handler)
        self.connect(self.burst_handler, self)
class Receiver(gr.hier_block2):
    def __init__(self):
        gr.hier_block2.__init__(self, "ofdm_rx",
					gr.io_signature(1, 1, gr.sizeof_gr_complex),
                    			gr.io_signature(1, 1, gr.sizeof_char))
        self.detector        = digital.ofdm_sync_sc_cfb(config.get_fft_length(), config.get_cp_length(), False, 0.95) 
        self.connect(self,self.detector)
        self.mixer   = blocks.multiply_cc()
        self.delay_block     = blocks.delay(gr.sizeof_gr_complex, config.get_fft_length() + config.get_cp_length() + SAFETY) #delay one ofdm symbol to get both preambles for channel estimation 
        self.oscillator      = analog.frequency_modulator_fc(-2.0 / config.get_fft_length())
        self.connect(self,self.delay_block)
        self.connect((self.detector,0), self.oscillator)
        self.connect(self.delay_block, (self.mixer,0))
        self.connect(self.oscillator, (self.mixer,1))   
        self.frame_filter    =  aux.filter_frame_cvc(config.get_frame_length(), config.get_fft_length(), config.get_cp_length())
        #self.connect(self.frame_filter,blocks.file_sink(gr.sizeof_gr_complex*config.get_fft_length(),"result.dat"))
        self.connect(self.mixer, (self.frame_filter,0))
        self.connect((self.detector,1), (self.frame_filter,1))
        self.framer          = blocks.stream_to_tagged_stream(gr.sizeof_gr_complex, config.get_fft_length(), config.get_frame_length() , LEN_TAG_KEY)
        self.fft_block       = fft.fft_vcc(config.get_fft_length(), True, (), True)
        self.connect(self.frame_filter,self.fft_block)		
        self.chanest         = digital.ofdm_chanest_vcvc(config.get_sync_word_one(),config.get_sync_word_two(), config.get_number_of_data_symbols())
        self.connect((self.fft_block), self.chanest)
        self.equalizer     = digital.ofdm_equalizer_simpledfe(
	            config.get_fft_length(),
	            config.get_constellation().base(),
	            config.get_data_tones(),
	            config.get_pilot_tones(),
	            config.get_pilot_symbols(),
	            symbols_skipped=0,
        )
        self.equalizer_block = digital.ofdm_frame_equalizer_vcvc(
	            self.equalizer.base(),
	            config.get_cp_length(),
	            LEN_TAG_KEY,
	            True,
	            config.get_number_of_data_symbols() # Header is 1 symbol long
        )
        self.connect(self.chanest, self.equalizer_block) 		
        self.serializer = digital.ofdm_serializer_vcc(
		           config.get_fft_length(), config.get_data_tones(),
		           LEN_TAG_KEY
        )
        self.connect(self.equalizer_block, self.serializer)
        self.demod      = digital.constellation_decoder_cb(config.get_constellation().base())
        self.repack     = blocks.repack_bits_bb(config.get_bits_per_symbol(), 8, LEN_TAG_KEY, True)
        self.connect( self.serializer, self.demod, self.repack)
        self.decoderf    = aux.decoder_reed_solomon_bb()
        self.commit_unt = aux.commit_to_output_bb()
        self.connect(self.repack, (self.decoderf,0), (self.commit_unt,0), self)
        self.connect((self.decoderf,1), (self.commit_unt,1))               
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		  
