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

#ifndef INCLUDED_ELECTROSENSE_DISCARD_SAMPLES_IMPL_H
#define INCLUDED_ELECTROSENSE_DISCARD_SAMPLES_IMPL_H

#include <electrosense/discard_samples.h>

namespace gr {
  namespace electrosense {

    class discard_samples_impl : public discard_samples
    {
     private:
      
     bool d_var_changed;
     bool d_tag_found;
     bool d_enable_varchange;
     double d_var;
     double d_nsamples;
     double d_cnt;
	 pmt::pmt_t d_tag_name;
	 gr::thread::mutex d_mutex;

     public:
      discard_samples_impl(double nsamples, double var, pmt::pmt_t tag_name, bool mode);
      ~discard_samples_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);
      
	  // callbacks
      void set_var(double var)
	  {
      	  gr::thread::scoped_lock guard(d_mutex);
		  discard_samples_impl::d_var = var;
		  discard_samples_impl::d_var_changed = true;
	  }

      void set_nsamples(double nsamples)
	  {
      	  gr::thread::scoped_lock guard(d_mutex);
		  discard_samples_impl::d_nsamples = nsamples;
	  }

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);
    };

  } // namespace electrosense
} // namespace gr

#endif /* INCLUDED_ELECTROSENSE_DISCARD_SAMPLES_IMPL_H */

