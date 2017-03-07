#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# 
# Copyright 2016 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import io
import time
import math 
import avro.schema
import avro.io
import socket
import ssl
import sys
import struct
import numpy as np
from gnuradio import gr

class sensor_sink(gr.sync_block):
    """
    docstring for block sensor_sink
    """
    def __init__(self, server, port, veclen,
                 dtype, avrofile, keyfile, certfile, senid, hopping, 
                 window, fftsize, avgfactor,
                 freqoverlap, freqresol, 
                 freq, gain):

        gr.sync_block.__init__(self,
            name="sensor_sink",
            in_sig=[(np.dtype(dtype),veclen)],
            out_sig=None)

        self.server = server
        self.port   = port
        self.avrofile = avrofile
        self.senid  = senid
        self.hopping = hopping
        self.window = window
        self.fftsize = fftsize
        self.avgfactor = avgfactor
        self.freqoverlap = freqoverlap
        self.freqresol  = freqresol
        self.freq = freq
        self.gain = gain
        self.certpath=certfile
        self.keypath=keyfile

        self.server_connect()
        self.init_packetizer()


    def set_hopping(self, hopping):
        self.hopping = hopping

    def set_window(self, window):
        self.window = window 

    def set_fftsize(self, fftsize):
        self.fftsize = fftsize

    def set_avgfactor(self, avgfactor):
        self.avgfactor = avgfactor

    def set_freqoverlap(self, freqoverlap):
        self.freqoverlap = freqoverlap

    def set_freqresol(self, freqresol):
        self.freqresol  = freqresol

    def set_freq(self, freq):
        self.freq = freq

    def set_gain(self, gain):
        self.gain = gain

    def get_constants(self, prefix):
        """Create a dictionary mapping socket module constants to their names."""
        return dict( (getattr(socket, n), n)
                for n in dir(socket)
                if n.startswith(prefix)
                )

    def server_connect(self):
        families = self.get_constants('AF_')
        types = self.get_constants('SOCK_')
        protocols = self.get_constants('IPPROTO_')
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.wrapped_socket = ssl.wrap_socket(self.sock,keyfile=self.keypath,certfile=self.certpath)
            ret = self.wrapped_socket.connect((self.server, self.port))
            self.sock = self.wrapped_socket
        except Exception as e:
            print("In server %s:%d. Exception is %s" % (self.server, self.port, e))

    def init_packetizer(self):
        self.schema = avro.schema.parse(open(self.avrofile).read())

    def packetize(self, data):
        self.bytes_writer = io.BytesIO()
        self.encoder = avro.io.BinaryEncoder(self.bytes_writer)
        self.writer = avro.io.DatumWriter(self.schema)
        ctime=math.modf(time.time())
        self.writer.write({"SenId": self.senid, 
                "SenConf":{"HoppingStrategy": self.hopping, "WindowingFunction": self.window, 
                "FFTSize": self.fftsize, "AveragingFactor": self.avgfactor, 
                "FrequencyOverlap": self.freqoverlap,
                "FrequencyResolution": self.freqresol, "Gain": self.gain }, 
                "SenTime":{"TimeSecs": int(ctime[1]), "TimeMicrosecs":int(round(ctime[0]*1e6))}, 
                "SenData":{"CenterFreq":self.freq, "SquaredMag": data.tolist()}}, self.encoder)
        raw_bytes = self.bytes_writer.getvalue()
        pktlen=int(len(raw_bytes))
        redfft=int((1-0.5)*(self.fftsize))
        extra = pktlen%4
        if extra: 
            pktlen=pktlen+(4-extra)
            raw_bytes=raw_bytes+struct.pack('!I', 0)[0:(4-extra)]
        message = struct.pack('!I', pktlen)+struct.pack('!I', redfft)+raw_bytes 
        return message

    def work(self, input_items, output_items):
        in0 = input_items[0]
        for i in range(in0.shape[0]):
            message = self.packetize(in0[i])
            #self.sock.sendall(message)
            self.sock.send(message)
        return len(input_items[0])

