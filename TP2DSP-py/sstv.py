#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  sstv.py
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
from PIL import Image
from synthesizer import Synthesizer
from recorder import Recorder
from math import sin, pi
import pdb

SAMPLE_RATE = 48000


class SSTV:
    #   Mode   Color  LPM          HSync  G (ms)  B (ms)  R (ms)  Space  VIS
    #          0      1            2      3       4       5       6      7
    NORMS = {
        "M1": ("GBR", 134.3947532, 4.862, 73.216, 73.216, 73.216, 0.562, 0x2C),
        'M2': ("GBR", 264.5525975, 4.862, 73.216, 73.216, 73.216, 0.562, 0x28),
    }

    def __init__(self, fs = 48000, mode = "M2"):
        self.fs = fs
        self.mode = mode

        self.gen_t = 0
        self.gen_phase = 0


    def sinegen(self, freq, period_ms):
        sig = []
        dt = 1 / self.fs
        dphase = 2 * pi * freq * dt
        end_t = self.gen_t + period_ms/1000

        while self.gen_t < end_t:
            sig.append(sin(self.gen_phase))
            self.gen_t += dt
            self.gen_phase += dphase

        return sig



    def sync(self, time = 5):
        return self.sinegen(1200, self.NORMS[self.mode][2])


    def video(self, time, level = 0):
        freq = 1500 + 800 * level

        return self.sinegen(freq, time)


    def VIS(self):
        id = self.NORMS[self.mode][7]
        # Sync
        signal = self.sinegen(1200, 30)
        # ID
        one_bits = 0
        for bitnr in range(7):
            if (id % 2) == 1:
                one_bits += 1
                signal += self.sinegen(1100, 30)
            else:
                signal += self.sinegen(1300, 30)
            id >>= 1

        if (one_bits % 2) == 1:
            signal += self.sinegen(1100, 30)
        else:
            signal += self.sinegen(1300, 30)
        # Sync
        signal = self.sinegen(1200, 30)
        return signal


    def color_bars(self, r, g, b):
        nr_bars = 10
        signal = self.VIS()
        norm = self.NORMS[self.mode]
        for lnr in range(256):
            signal += self.sync(norm[2])
            signal += self.video(norm[6], 0)
            for l in range(nr_bars):
                signal += self.video(norm[3]/nr_bars, l/(nr_bars-1))
            signal += self.video(norm[6], 0)
            signal += self.video(norm[4], 0)
            signal += self.video(norm[6], 0)
            for l in range(nr_bars):
                signal += self.video(norm[5]/nr_bars, l/(nr_bars-1))
            signal += self.video(norm[6], 0)
        return signal


    def png_image(self, img):
        img = Image.open(img)
        print(img.size)
        norm = self.NORMS[self.mode]
        if img.size != (320, 256):
            print("Tamaño de la imagen debe ser 320x256")
            exit(-1)

        tpix = 0.457641     # 0.460025

        signal = self.VIS()
        for y in range(256):
            signal += self.sync(norm[2])
            signal += self.video(self.NORMS[self.mode][6], 0)
            for x in range(320):
                pix = img.getpixel((x, y))
                signal += self.video(tpix, pix[1]/255)
            signal += self.video(norm[6], 0)
            for x in range(320):
                pix = img.getpixel((x, y))
                signal += self.video(tpix, pix[2]/255)
            signal += self.video(norm[6], 0)
            for x in range(320):
                pix = img.getpixel((x, y))
                signal += self.video(tpix, pix[0]/255)
            signal += self.video(norm[6], 0)
        return signal


def test_new_gen():
    sstv = SSTV(mode = "M1")
    samples = sstv.sinegen(1200, 0.3) + sstv.sinegen(2200, 0.3)
    plt.plot(samples)
    plt.show()


def make_color_bars():
    sstv = SSTV(mode = "M2")
    signal = sstv.color_bars(1, 0.5, 0)
    print(len(signal))

    rec = Recorder()
    rec.record("sync.wav", signal)


def make_image():
    img = "ucc_320x256.a.jpg"
    img = "grays_320x256.jpg"
    sstv = SSTV(mode = "M1")
    signal = sstv.png_image(img)

    rec = Recorder()
    rec.record("image.wav", signal)


def main(args):
    # ~ test_new_gen()
    # ~ make_color_bars()
    make_image()
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
