from gnuradio import gr,blocks, channels,digital
import rxtx_ofdm as o
from gnuradio import iio

TRANSMITTER       = "192.168.2.1"
RECEIVER          = "192.168.0.10"
CENTRAL_FREQUENCY = 1800000000
SAMPLE_RATE       = 4000000         
BANDWIDTH_RF      = 4000000       
BUFFER_SIZE       = 0x8000
ATTENUATION       = 0
FILTER            = ''
AUTO_FILTER       = False 
QUADRA_TRACKING   = True 
DC_TRACKING       = True
BB_TRACKING       = True
GAIN_MODE         = "manual"
MANUAL_GAIN       = 50


class test_bench_radio(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        udp_sink    = blocks.udp_sink(1,"192.168.0.1", 9991, 1)
        ofdm_recv   = o.Receiver()
        radio       = iio.pluto_source(RECEIVER, CENTRAL_FREQUENCY,
                                           SAMPLE_RATE,
                                           BANDWIDTH_RF, 
                                           BUFFER_SIZE,
                                           QUADRA_TRACKING,
                                           DC_TRACKING,
                                           BB_TRACKING,
                                           GAIN_MODE,
                                           MANUAL_GAIN,
                                           FILTER,
                                           AUTO_FILTER)
        self.connect(radio, ofdm_recv, udp_sink) 
    def closeEvent(self, event):
    	event.accept() 
tunnel = test_bench_radio()
tunnel.run()
