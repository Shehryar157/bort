# -*- coding: utf-8 -*-
# BGT-ish Sound_lib wrapper
# Original author: Carter Temm
# Edited by Yukio Nozawa <personal@nyanchangames.com>
# License: GPL V2.0 (See copying.txt for details)

import math
import sound_lib
import sound_lib.output
import sound_lib.sample
from sound_lib import stream
s = sound_lib.output.Output()


class sound():
    def __init__(self):
        self.handle = None
        self.freq = 44100
        self.paused = False

    def stream(self, filename=""):
        if self.handle:
            self.close()
# end close previous
        self.handle = stream.FileStream(file=filename)
        self.freq = self.handle.get_frequency()

    def load(self, sample=None):
        if self.handle:
            self.close()
# end close previous
        self.handle = sound_lib.sample.SampleBasedChannel(sample)
        self.freq = self.handle.get_frequency()

    def play(self):
        self.handle.looping = False
        self.handle.play()

    def setPaused(self, p):
        if self.paused == p:
            return
        if not self.playing and p:
            return
        self.paused = p
        if p:
            self.handle.pause()
        else:
            self.handle.play()
        # end pause or unpause
    # end setPaused

    def play_wait(self):
        self.handle.looping = False
        self.handle.play_blocking()

    def play_looped(self):
        self.handle.looping = True
        self.handle.play()

    def stop(self):
        if self.handle and self.handle.is_playing:
            self.handle.stop()
            self.handle.set_position(0)

    def fadein(self, vol = 100, fadetime = 500):
        """The faded sound might be kept playing internally. Make sure that you call stop() before fading in or playing again. Fading will be performed by BASS's internal thread, so playing this instance after calling fadeout() may sound strangely."""
        if self.handle and self.handle.is_playing:
            self.handle.slide_attribute("volume", vol, fadetime)

    def fadeout(self, fadetime):
        """The faded sound might be kept playing internally. Make sure that you call stop() before fading in or playing again. Fading will be performed by BASS's internal thread, so playing this instance after calling fadeout() may sound strangely."""
        if self.handle and self.handle.is_playing:
            self.handle.slide_attribute("volume", 0, fadetime)

    @property
    def volume(self):
        if not self.handle:
            return False
        return round(math.log10(self.handle.volume) * 20)

    @volume.setter
    def volume(self, value):
        if not self.handle:
            return False
        res = value / 100
        self.handle.set_volume(res)

    @property
    def pitch(self):
        if not self.handle:
            return False
        return (self.handle.get_frequency() / self.freq) * 100

    @pitch.setter
    def pitch(self, value):
        if value > 400:
            value = 400
        if not self.handle:
            return False
        self.handle.set_frequency((float(value) / 100) * self.freq)

    @property
    def pan(self):
        if not self.handle:
            return False
        return self.handle.get_pan() * 100

    @pan.setter
    def pan(self, value):
        if not self.handle:
            return False
        self.handle.set_pan(float(value) / 100)

    @property
    def playing(self):
        if self.handle is None:
            return False
        try:
            s = self.handle.is_playing
        except BassError:
            return False
        # end try
        return s

    def close(self):
        if self.handle:
            self.handle.free()
    def pan_sound(listenerx, listenery, sourcex, sourcey, channels=10, volchange=10):
        Hdirection=None
        if listenerx>sourcex:
            value=listenerx-sourcex
            Hdirection="left"
        else:
            value=sourcex-listenerx
            Hdirection="right"
        if Hdirection=="left":
            if value>channels:
                return 0, 0
            else:
                var1=-value*100/channels
        else:
            if value>channels:
                return 0, 0
            else:
                var1=value*100/channels
        if listenery>sourcey:
            value=listenery-sourcey
        else:
            value=sourcey-listenery
        if value>volchange:
            return 0, 0
        else:
            var2=100-(value*100/volchange)
        return var1, var2


# helper functions


def playOneShot(sample, vol=0, pitch=100):
    s = sound()
    s.load(sample)
    s.volume = vol
    s.pitch = pitch
    s.play()
