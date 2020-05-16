from gnuradio import gr,blocks, channels, digital
import rxtx_ofdm as o
import random
from gnuradio import iio
LEN_TAG_KEY = "packet_length"
TRANSMITTER       = "192.168.0.10"
RECEIVER          = "192.168.3.2"
CENTRAL_FREQUENCY = 1700000000
SAMPLE_RATE       = 4200000#8500000
BANDWIDTH_RF      = 4200000#8500000
BUFFER_SIZE       = 4*26*8*10
ATTENUATION       = 0
FILTER            = ''
AUTO_FILTER       = True 
QUADRA_TRACKING   = DC_TRACKING = BB_TRACKING = True 
GAIN_MODE         = "manual"
MANUAL_GAIN       = 64.0


class test_bench_radio(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        udp_source  = blocks.udp_source(1,"192.168.0.1", 9990, 4)
        #ofdm_trans = digital.ofdm_txrx.ofdm_tx()
        ofdm_trans  = o.Transmitter()
        radio       = iio.pluto_sink(TRANSMITTER,CENTRAL_FREQUENCY,
                                                SAMPLE_RATE,
                                                BANDWIDTH_RF,
                                                BUFFER_SIZE,
                                                False,
                                                ATTENUATION,
                                                FILTER,
                                                AUTO_FILTER)
        self.connect(udp_source,ofdm_trans, radio)
        #self.connect(ofdm_trans, blocks.file_sink(gr.sizeof_gr_complex,"transmitted.dat"))
    def closeEvent(self, event):
    	event.accept() 
tunnel = test_bench_radio()
tunnel.run()
