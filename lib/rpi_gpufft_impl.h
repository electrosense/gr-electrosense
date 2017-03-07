/* -*- c++ -*- */
/* 
 * Copyright 2016 <+YOU OR YOUR COMPANY+>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifndef INCLUDED_ELECTROSENSE_RPI_GPUFFT_IMPL_H
#define INCLUDED_ELECTROSENSE_RPI_GPUFFT_IMPL_H

#include <electrosense/rpi_gpufft.h>

extern "C" {
#include "gpu_fft.h"	
#include "mailbox.h"	
}

namespace gr {
  namespace electrosense {

    class rpi_gpufft_impl : public rpi_gpufft
    {
     private:
	 
		int d_fft_size;
		bool d_forward;
		bool d_shift;
		int d_njobs;
		int d_mb;
    	struct GPU_FFT_COMPLEX *d_base;
    	struct GPU_FFT *d_fft;



     public:
      rpi_gpufft_impl(int fft_size, bool forward,
							  bool shift, int njobs);
      ~rpi_gpufft_impl();

      int work(int noutput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
    };

  } // namespace electrosense
} // namespace gr

#endif /* INCLUDED_ELECTROSENSE_RPI_GPUFFT_IMPL_H */

