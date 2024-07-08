#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  demo_syn.py
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
from random import random


class Synthesizer():
    def __init__(self, fs = 48000):
        self.fs = fs


    def sine(self, f = 1000, phase = 0):
        dphase = f/self.fs * 2 * np.pi
        phase = phase

        while True:
            new_freq = yield np.sin(phase)
            if new_freq is not None:
                dphase = new_freq/self.fs * 2 * np.pi
            phase += dphase


    def cosine(self, f = 1000, phase = 0):
        dphase = f/self.fs * 2 * np.pi
        phase = phase

        while True:
            new_freq = yield np.cos(phase)
            if new_freq is not None:
                dphase = new_freq/self.fs * 2 * np.pi
            phase += dphase


    def sine_t(self, f = 1000, phase = 0):
        dt = 1/self.fs
        t = 0

        while True:
            new_freq = yield t, np.sin(f*t * 2 * np.pi + phase)
            if new_freq is not None:
                f = new_freq
            t += dt


    def square(self, f = 1000, phase = 0, dutycycle = 0.5):
        pass


    def triangle(self, f = 1000, phase = 0, dutycycle = 0.5):
        pass


    # Non periodicas
    def noise(self):
        while True:
            yield random() * 2 - 1


    def pulse(self, initial = 0, format = [], min = 0, max = 1):
        pass


    def chirp(self, fstart = 100, fend =1000, steps = 1000):
        log_fstart = np.log(fstart)
        log_fend = np.log(fend)
        log_delta = (log_fend - log_fstart) / steps
        factor = np.exp(log_delta)
        phase = 0
        f = fstart

        while f <= fend:
            yield np.sin(phase)
            f *= factor
            phase += 2 * np.pi * f / self.fs



def test_sine():
    syn = Synthesizer()
    sin_gen = syn.sine(f = 1000, phase = 0)

    s = [next(sin_gen) for i in range(48)]
    print(s)

    plt.plot(s)
    plt.show()


def test_sine2():
    syn = Synthesizer()
    sin_gen = syn.sine(f = 1000, phase = 0)

    s = [next(sin_gen) for i in range(48)]
    s += [sin_gen.send(2300)] + [next(sin_gen) for i in range(48)]

    plt.plot(s)
    plt.show()


def test_sine_t():
    syn = Synthesizer()
    sin_gen = syn.sine_t(f = 1000, phase = 0)

    s = [next(sin_gen) for i in range(48)]
    print(s)

    plt.plot(*zip(*s), ".")
    plt.show()


def test_random():
    syn = Synthesizer()
    rnd_gen = syn.noise()
    for p in range(10):
        print(next(rnd_gen))


def test_chirp():
    syn = Synthesizer()
    chirp_gen = syn.chirp(100, 1000, 1000)
    signal = [s for s in chirp_gen]
    plt.plot(signal)
    plt.show()


def main(args):
    # ~ test_sine()
    test_sine2()
    # ~ test_sine_t()
    # ~ test_random()
    # ~ test_chirp()
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
