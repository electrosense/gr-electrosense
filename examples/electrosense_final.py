#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Electosense
# Author: Sreeraj Rajendran
# Description: Electrosense sensor code
# Generated: Tue Mar  7 11:29:17 2017
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import fft
from gnuradio import filter
from gnuradio import gr
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from optparse import OptionParser
import electrosense
import pmt
import scanning  # embedded python module
import sys
import threading
import time


class electrosense_final(gr.top_block, Qt.QWidget):

    def __init__(self, end_f=2000e6, start_f=50e6):
        gr.top_block.__init__(self, "Electosense")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Electosense")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "electrosense_final")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Parameters
        ##################################################
        self.end_f = end_f
        self.start_f = start_f

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 5e6
        self.prober = prober = 1
        self.hop_mode = hop_mode = 0
        self.tune_delay = tune_delay = 20e-3
        self.sensorid = sensorid = 123456
        self.rfgain = rfgain = 40
        self.ppm = ppm = 0
        self.navg_vectors = navg_vectors = 50
        self.fft_size = fft_size = 4096
        self.cfreq = cfreq = scanning.step(start_f,end_f,samp_rate/1.5,prober,hop_mode,0.8,0.8)
        self.alpha = alpha = 0.75

        ##################################################
        # Blocks
        ##################################################
        self.vecprobe = blocks.probe_signal_vf(fft_size)
        self.uhd_usrp_source_0 = uhd.usrp_source(
        	",".join(("addr=192.168.10.2", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_center_freq(cfreq, 0)
        self.uhd_usrp_source_0.set_gain(35, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.single_pole_iir_filter_xx_0 = filter.single_pole_iir_filter_ff(alpha, fft_size)
        
        def _prober_probe():
            while True:
                val = self.vecprobe.level()
                try:
                    self.set_prober(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (1/(tune_delay+(1/samp_rate*fft_size*navg_vectors))))
        _prober_thread = threading.Thread(target=_prober_probe)
        _prober_thread.daemon = True
        _prober_thread.start()
            
        self.fft_vxx_0 = fft.fft_vcc(fft_size, True, (window.blackmanharris(fft_size)), True, 1)
        self.electrosense_sensor_sink_0 = electrosense.sensor_sink("collector.electrosense.org", 5000, fft_size,
                         "float32", "/home/rsreeraj/gnu_work/gr-electrosense/python/rtl-spec.avsc", "/home/rsreeraj/gnu_work/gr-electrosense/python/sensor_cert/Sensor-SSL-SK.pem", "/home/rsreeraj/gnu_work/gr-electrosense/python/sensor_cert/Sensor-SSL-Cert.pem", sensorid, 0, 
                         2, fft_size, int(3/alpha),
                         0.1, int(samp_rate/fft_size), 
                         int(cfreq), rfgain)
        self.electrosense_discard_samples_0 = electrosense.discard_samples(int(tune_delay * samp_rate), int(cfreq), pmt.intern("burst_len"), False)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fft_size)
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_float*fft_size, navg_vectors)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(fft_size)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.single_pole_iir_filter_xx_0, 0))    
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.electrosense_sensor_sink_0, 0))    
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.vecprobe, 0))    
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))    
        self.connect((self.electrosense_discard_samples_0, 0), (self.blocks_stream_to_vector_0, 0))    
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))    
        self.connect((self.single_pole_iir_filter_xx_0, 0), (self.blocks_keep_one_in_n_0, 0))    
        self.connect((self.uhd_usrp_source_0, 0), (self.electrosense_discard_samples_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "electrosense_final")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_end_f(self):
        return self.end_f

    def set_end_f(self, end_f):
        self.end_f = end_f
        self.set_cfreq(scanning.step(self.start_f,self.end_f,self.samp_rate/1.5,self.prober,self.hop_mode,0.8,0.8))

    def get_start_f(self):
        return self.start_f

    def set_start_f(self, start_f):
        self.start_f = start_f
        self.set_cfreq(scanning.step(self.start_f,self.end_f,self.samp_rate/1.5,self.prober,self.hop_mode,0.8,0.8))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_cfreq(scanning.step(self.start_f,self.end_f,self.samp_rate/1.5,self.prober,self.hop_mode,0.8,0.8))
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
        self.electrosense_sensor_sink_0.set_freqresol(int(self.samp_rate/self.fft_size))
        self.electrosense_discard_samples_0.set_nsamples(int(self.tune_delay * self.samp_rate))

    def get_prober(self):
        return self.prober

    def set_prober(self, prober):
        self.prober = prober
        self.set_cfreq(scanning.step(self.start_f,self.end_f,self.samp_rate/1.5,self.prober,self.hop_mode,0.8,0.8))

    def get_hop_mode(self):
        return self.hop_mode

    def set_hop_mode(self, hop_mode):
        self.hop_mode = hop_mode
        self.set_cfreq(scanning.step(self.start_f,self.end_f,self.samp_rate/1.5,self.prober,self.hop_mode,0.8,0.8))

    def get_tune_delay(self):
        return self.tune_delay

    def set_tune_delay(self, tune_delay):
        self.tune_delay = tune_delay
        self.electrosense_discard_samples_0.set_nsamples(int(self.tune_delay * self.samp_rate))

    def get_sensorid(self):
        return self.sensorid

    def set_sensorid(self, sensorid):
        self.sensorid = sensorid

    def get_rfgain(self):
        return self.rfgain

    def set_rfgain(self, rfgain):
        self.rfgain = rfgain
        self.electrosense_sensor_sink_0.set_gain(self.rfgain)

    def get_ppm(self):
        return self.ppm

    def set_ppm(self, ppm):
        self.ppm = ppm

    def get_navg_vectors(self):
        return self.navg_vectors

    def set_navg_vectors(self, navg_vectors):
        self.navg_vectors = navg_vectors
        self.blocks_keep_one_in_n_0.set_n(self.navg_vectors)

    def get_fft_size(self):
        return self.fft_size

    def set_fft_size(self, fft_size):
        self.fft_size = fft_size
        self.electrosense_sensor_sink_0.set_fftsize(self.fft_size)
        self.electrosense_sensor_sink_0.set_freqresol(int(self.samp_rate/self.fft_size))

    def get_cfreq(self):
        return self.cfreq

    def set_cfreq(self, cfreq):
        self.cfreq = cfreq
        self.uhd_usrp_source_0.set_center_freq(self.cfreq, 0)
        self.electrosense_sensor_sink_0.set_freq(int(self.cfreq))
        self.electrosense_discard_samples_0.set_var(int(self.cfreq))

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.single_pole_iir_filter_xx_0.set_taps(self.alpha)
        self.electrosense_sensor_sink_0.set_avgfactor(int(3/self.alpha))


def argument_parser():
    description = 'Electrosense sensor code'
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option, description=description)
    parser.add_option(
        "", "--end-f", dest="end_f", type="eng_float", default=eng_notation.num_to_str(2000e6),
        help="Set End Frequency [default=%default]")
    parser.add_option(
        "", "--start-f", dest="start_f", type="eng_float", default=eng_notation.num_to_str(50e6),
        help="Set Start frequency [default=%default]")
    return parser


def main(top_block_cls=electrosense_final, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(end_f=options.end_f, start_f=options.start_f)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
