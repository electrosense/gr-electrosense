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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "discard_samples_impl.h"

namespace gr {
  namespace electrosense {

    discard_samples::sptr
    discard_samples::make(double nsamples, double var, pmt::pmt_t tag_name, bool mode)
    {
      return gnuradio::get_initial_sptr
        (new discard_samples_impl(nsamples, var, tag_name, mode));
    }

    /*
     * The private constructor
     */
    discard_samples_impl::discard_samples_impl(double nsamples, double var, pmt::pmt_t tag_name, bool mode)
      : gr::block("discard_samples",
              gr::io_signature::make(1, 1, sizeof(gr_complex)),
              gr::io_signature::make(1, 1, sizeof(gr_complex))),
	 		  d_nsamples(nsamples),
	 		  d_var(var),
	 		  d_tag_name(tag_name),
	 		  d_cnt(0),
	 		  d_enable_varchange(true),
	 		  d_var_changed(false),
	 		  d_tag_found(false)
    {

		if(mode)
		{
	 	  d_enable_varchange = false;
		}
		else
		{
	 	  d_enable_varchange = true;
		}


	}

    /*
     * Our virtual destructor.
     */
    discard_samples_impl::~discard_samples_impl()
    {
    }

    void
    discard_samples_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      ninput_items_required[0] = noutput_items; 
    }

	int
		discard_samples_impl::general_work (int noutput_items,
				gr_vector_int &ninput_items,
				gr_vector_const_void_star &input_items,
				gr_vector_void_star &output_items)
		{
			gr::thread::scoped_lock guard(d_mutex);
			const gr_complex *in = (const gr_complex *) input_items[0];
			gr_complex *out = (gr_complex *) output_items[0];

			if(d_enable_varchange)
			{
				if(d_var_changed)
				{
					//std::cout << "variable change" <<std::endl;
					//delete nsamples here
					int minsamp = std::min((double)ninput_items[0],(d_nsamples-d_cnt));
					d_cnt = d_cnt + minsamp;
					consume_each(minsamp);
					//disable after deleting d_nsamples
					if (d_cnt >= d_nsamples)
					{
						d_var_changed=false;
						d_cnt=0;
					}
					//std::cout << "Deleting:"<< minsamp <<std::endl;
					return 0;
				}
				else
				{
					//copy to out buffer
					std::memcpy(out, in, noutput_items * sizeof(gr_complex));
					consume_each(noutput_items);
					//std::cout << "copying"<< noutput_items <<std::endl;
					return noutput_items;
				}
			}
			else
			{
				std::vector<gr::tag_t> tags;
				const uint64_t nread = nitems_read(0);

				//search for tags
				get_tags_in_range(tags, 0, nread, nread + noutput_items, d_tag_name);
				std::sort(tags.begin(), tags.end(), tag_t::offset_compare);

				//copy buffers till the tag to out and enable tag_found
				if(tags.size()) {
					tag_t tag = tags.front();
					if(tag.offset == nitems_read(0)) {
						d_tag_found=true;
						//std::cout << "Tag found"<<std::endl;
					}
					else {
						uint64_t cpy = std::min((uint64_t)noutput_items, tag.offset - nitems_written(0));
						std::memcpy(out, in, cpy * sizeof(gr_complex));
						consume_each(cpy);
						//std::cout << "copying"<< cpy <<std::endl;
						return cpy;
					} 
				}
				if(d_tag_found) {
					int minsamp = std::min((double)ninput_items[0], (d_nsamples-d_cnt));
					d_cnt = d_cnt + minsamp;
					consume_each(minsamp);
					//disable after deleting
					if (d_cnt >= d_nsamples)
					{
						d_tag_found=false;
						d_cnt=0;
					}
					//std::cout << "Deleting:"<< minsamp <<std::endl;
					return 0;
				} else {
					std::memcpy(out, in, noutput_items * sizeof(gr_complex));
					consume_each(noutput_items);
					//std::cout << "copying"<< noutput_items <<std::endl;
					return noutput_items;
				}   
			}
		}



  } /* namespace electrosense */
} /* namespace gr */

