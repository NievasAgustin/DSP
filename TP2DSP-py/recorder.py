#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  recorder.py
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


import pylab as plt
import numpy as np
import scipy

import soundfile as sf

TEST_AUDIO = "cw20.wav"

class Recorder():
    def __init__(self, fs = 48000):
        self.fs = fs


    def record(self, fname, samples):
        sf.write(fname, samples, self.fs)


    def play(self, fname):
        return sf.read(fname)


def test_read():
    rec = Recorder()
    samples, framerate = rec.play(TEST_AUDIO)
    # ~ print(list(samples))
    plt.plot(samples)
    plt.show()



def main(args):
    test_read()
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
