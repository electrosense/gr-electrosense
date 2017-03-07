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


#ifndef INCLUDED_ELECTROSENSE_DISCARD_SAMPLES_H
#define INCLUDED_ELECTROSENSE_DISCARD_SAMPLES_H

#include <electrosense/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace electrosense {

    /*!
     * \brief <+description of block+>
     * \ingroup electrosense
     *
     */
    class ELECTROSENSE_API discard_samples : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<discard_samples> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of electrosense::discard_samples.
       *
       * To avoid accidental use of raw pointers, electrosense::discard_samples's
       * constructor is in a private implementation
       * class. electrosense::discard_samples::make is the public interface for
       * creating new instances.
       */
      static sptr make(double nsamples, double var, pmt::pmt_t tag_name, bool mode);

	  virtual void set_nsamples(double d_nsamples) = 0;
	  virtual void set_var(double d_var) = 0;
    };

  } // namespace electrosense
} // namespace gr

#endif /* INCLUDED_ELECTROSENSE_DISCARD_SAMPLES_H */

