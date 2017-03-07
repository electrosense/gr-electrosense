#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Electosense
# Author: Sreeraj Rajendran
# Description: Electrosense sensor code
# Generated: Mon Aug 29 13:51:32 2016
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
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import electrosense
import osmosdr
import sys


class electrosense_sink_test(gr.top_block, Qt.QWidget):

    def __init__(self):
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

        self.settings = Qt.QSettings("GNU Radio", "electrosense_sink_test")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.sensorid = sensorid = 123456
        self.samp_rate = samp_rate = 2e6
        self.ppm_slider = ppm_slider = 0
        self.g_slider = g_slider = 0
        self.fft_size = fft_size = 512
        self.fc_slider = fc_slider = 100e6
        self.alpha = alpha = 0.5

        ##################################################
        # Blocks
        ##################################################
        self._ppm_slider_range = Range(-150, 150, 1, 0, 200)
        self._ppm_slider_win = RangeWidget(self._ppm_slider_range, self.set_ppm_slider, "ppm_slider", "counter_slider", float)
        self.top_layout.addWidget(self._ppm_slider_win)
        self._g_slider_range = Range(0, 50, 1, 0, 200)
        self._g_slider_win = RangeWidget(self._g_slider_range, self.set_g_slider, "g_slider", "counter_slider", float)
        self.top_layout.addWidget(self._g_slider_win)
        self._fc_slider_range = Range(52e6, 1.8e9, 500e3, 100e6, 200)
        self._fc_slider_win = RangeWidget(self._fc_slider_range, self.set_fc_slider, "fc_slider", "counter_slider", float)
        self.top_layout.addWidget(self._fc_slider_win)
        self.single_pole_iir_filter_xx_0 = filter.single_pole_iir_filter_ff(alpha, fft_size)
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(fc_slider, 0)
        self.rtlsdr_source_0.set_freq_corr(ppm_slider, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(2, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(2, 0)
        self.rtlsdr_source_0.set_gain_mode(True, 0)
        self.rtlsdr_source_0.set_gain(g_slider, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna("", 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)
          
        self.fft_vxx_0 = fft.fft_vcc(fft_size, True, (window.blackmanharris(fft_size)), True, 1)
        self.electrosense_sensor_sink_0 = electrosense.sensor_sink("127.0.0.1", 5000, fft_size,
                         "float32", "/home/rsreeraj/gnu_work/gr-electrosense/python/rtl-spec.avsc", sensorid, 0, 
                         2, fft_size, int(3/alpha),
                         0.1, int(samp_rate/fft_size), 
                         int(fc_slider), g_slider)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, fft_size)
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_float*fft_size, 100)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(fft_size)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.single_pole_iir_filter_xx_0, 0))    
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.electrosense_sensor_sink_0, 0))    
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))    
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_stream_to_vector_0, 0))    
        self.connect((self.single_pole_iir_filter_xx_0, 0), (self.blocks_keep_one_in_n_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "electrosense_sink_test")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_sensorid(self):
        return self.sensorid

    def set_sensorid(self, sensorid):
        self.sensorid = sensorid

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)
        self.electrosense_sensor_sink_0.set_freqresol(int(self.samp_rate/self.fft_size))

    def get_ppm_slider(self):
        return self.ppm_slider

    def set_ppm_slider(self, ppm_slider):
        self.ppm_slider = ppm_slider
        self.rtlsdr_source_0.set_freq_corr(self.ppm_slider, 0)

    def get_g_slider(self):
        return self.g_slider

    def set_g_slider(self, g_slider):
        self.g_slider = g_slider
        self.rtlsdr_source_0.set_gain(self.g_slider, 0)
        self.electrosense_sensor_sink_0.set_gain(self.g_slider)

    def get_fft_size(self):
        return self.fft_size

    def set_fft_size(self, fft_size):
        self.fft_size = fft_size
        self.electrosense_sensor_sink_0.set_fftsize(self.fft_size)
        self.electrosense_sensor_sink_0.set_freqresol(int(self.samp_rate/self.fft_size))

    def get_fc_slider(self):
        return self.fc_slider

    def set_fc_slider(self, fc_slider):
        self.fc_slider = fc_slider
        self.rtlsdr_source_0.set_center_freq(self.fc_slider, 0)
        self.electrosense_sensor_sink_0.set_freq(int(self.fc_slider))

    def get_alpha(self):
        return self.alpha

    def set_alpha(self, alpha):
        self.alpha = alpha
        self.single_pole_iir_filter_xx_0.set_taps(self.alpha)
        self.electrosense_sensor_sink_0.set_avgfactor(int(3/self.alpha))


def main(top_block_cls=electrosense_sink_test, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
