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

import numpy
import pmt
from gnuradio import gr

class variable_updater(gr.basic_block):
    """
    docstring for block variable_updater
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="variable_updater",
            in_sig=[],
            out_sig=[])

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.commdict = {"freq": lambda x: self.lserv.set_cfreq(float(x)),
                         "alpha": lambda x: self.lserv.set_alpha(float(x)),
                         "ppm": lambda x: self.lserv.set_ppm(float(x)),
                         "rfgain": lambda x: self.lserv.set_rfgain(int(x)),
                         "tune_delay": lambda x: self.lserv.set_tune_delay(float(x)),
                        }

    def register_instance(self,tb):
        self.lserv = tb

    def handle_msg(self, msg_pmt):
        msg = pmt.to_python(msg_pmt)
        if self.commdict.has_key(msg[0]):
            try:
                self.commdict[msg[0]](msg[1])
                print "Updating: ", msg
            except:
                print "Updating failed: ", msg

