/* -*- c++ -*- */

#define ELECTROSENSE_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "electrosense_swig_doc.i"

%{
#include "electrosense/discard_samples.h"
#include "electrosense/rpi_gpufft.h"
%}

%include "electrosense/discard_samples.h"
GR_SWIG_BLOCK_MAGIC2(electrosense, discard_samples);
%include "electrosense/rpi_gpufft.h"
GR_SWIG_BLOCK_MAGIC2(electrosense, rpi_gpufft);
