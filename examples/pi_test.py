#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Electosense
# Author: Sreeraj Rajendran
# Description: Electrosense sensor code
# Generated: Tue Aug 30 16:59:18 2016
##################################################

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import electrosense
import osmosdr
import pmt


class pi_test(gr.top_block):

    def __init__(self, rx_gain=50, tx_gain=5):
        gr.top_block.__init__(self, "Electosense")

        ##################################################
        # Parameters
        ##################################################
        self.rx_gain = rx_gain
        self.tx_gain = tx_gain

        ##################################################
        # Variables
        ##################################################
        self.sensorid = sensorid = 123456
        self.samp_rate = samp_rate = 1e6
        self.fft_size = fft_size = 512
        self.cfreq = cfreq = 100e6
        self.alpha = alpha = 0.5

        ##################################################
        # Blocks
        ##################################################
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(cfreq, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(2, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(2, 0)
        self.rtlsdr_source_0.set_gain_mode(True, 0)
        self.rtlsdr_source_0.set_gain(rx_gain, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna("", 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
          
        self.electrosense_rpi_gpufft_0 = electrosense.rpi_gpufft(512, True, True, 16)
        self.electrosense_discard_samples_0 = electrosense.discard_samples(100, int(cfreq), pmt.intern("burst_len"), False)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fft_size)
        self.blocks_null_sink_1 = blocks.null_sink(gr.sizeof_gr_complex*fft_size)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_stream_to_vector_0, 0), (self.electrosense_rpi_gpufft_0, 0))    
        self.connect((self.electrosense_discard_samples_0, 0), (self.blocks_stream_to_vector_0, 0))    
        self.connect((self.electrosense_rpi_gpufft_0, 0), (self.blocks_null_sink_1, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.electrosense_discard_samples_0, 0))    

    def get_rx_gain(self):
        return self.rx_gain

    def set_rx_gain(self, rx_gain):
        self.rx_gain = rx_gain
        self.rtlsdr_source_0.set_gain(self.rx_gain, 0)

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain

    def get_sensorid(self):
        return self.sensorid

    def set_sensorid(self, sensorid):
        self.sensorid = sensorid

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)

    def get_fft_size(self):
        return self.fft_size

    def set_fft_size(self, fft_size):
        self.fft_size = fft_size

    def get_cfreq(self):
        return self.cfreq

    def set_cfreq(self, cfreq):
        self.cfreq = cfreq
        self.rtlsdr_source_0.set_center_freq(self.cfreq, 0)
        self.electrosense_discard_samples_0.set_var(int(self.cfreq))

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha


def argument_parser():
    description = 'Electrosense sensor code'
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option, description=description)
    parser.add_option(
        "", "--rx-gain", dest="rx_gain", type="eng_float", default=eng_notation.num_to_str(50),
        help="Set RX Gain [default=%default]")
    parser.add_option(
        "", "--tx-gain", dest="tx_gain", type="eng_float", default=eng_notation.num_to_str(5),
        help="Set TX Gain [default=%default]")
    return parser


def main(top_block_cls=pi_test, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(rx_gain=options.rx_gain, tx_gain=options.tx_gain)
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
