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


#ifndef INCLUDED_ELECTROSENSE_RPI_GPUFFT_H
#define INCLUDED_ELECTROSENSE_RPI_GPUFFT_H

#include <electrosense/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace electrosense {

    /*!
     * \brief <+description of block+>
     * \ingroup electrosense
     *
     */
    class ELECTROSENSE_API rpi_gpufft : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<rpi_gpufft> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of electrosense::rpi_gpufft.
       *
       * To avoid accidental use of raw pointers, electrosense::rpi_gpufft's
       * constructor is in a private implementation
       * class. electrosense::rpi_gpufft::make is the public interface for
       * creating new instances.
       */
      static sptr make(int fft_size, bool forward,
							  bool shift, int njobs);
    };

  } // namespace electrosense
} // namespace gr

#endif /* INCLUDED_ELECTROSENSE_RPI_GPUFFT_H */

