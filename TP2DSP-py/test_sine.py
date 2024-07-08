#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  test_sine.py
#
#  Copyright 2020 John Coppens <john@jcoppens.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

import numpy as np
import simpleaudio as sa
from synthesizer import Synthesizer

SAMPLE_RATE = 48000

def main(args):
    synth = Synthesizer(fs = SAMPLE_RATE)
    sine_gen = synth.sine(1000)
    tone_1k = [int(32000*next(sine_gen)) for i in range(SAMPLE_RATE)]
    tone_1k = np.array(tone_1k, dtype = np.int16)
    # ~ print(tone_1k)

    sa.play_buffer(tone_1k, 1, 2, SAMPLE_RATE)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
