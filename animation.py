import math
import time
from color import *


class BaseAnimation(object):
    def __init__(self, led, start, end, concurrent=False, duration=0):
        self._led = led
        self._start = start
        self._end = end
        self.concurrent = concurrent
        if self._end == 0 or self._end > self._led.lastIndex:
            self._end = self._led.lastIndex

        self._size = self._end - self._start + 1
        self._step = 0
        self._duration = duration

    def step(self):
        raise RuntimeError("Base class step() called. This shouldn't happen")

    def run(self, sleep=None, max_steps = 0):
        cur_step = 0
        while max_steps == 0 or cur_step < max_steps:
            if self.step() == true:
                self._led.update()
                if sleep:
                    time.sleep(sleep)
                cur_step += 1
            else: 
                break
        #TODO Account for a duration in run time. 0=never end the float should be in seconds
        #TODO reconcile max steps

class Rainbow(BaseAnimation):
    """Generate rainbow."""

    def __init__(self, led, start=0, end=0):
        super(Rainbow, self).__init__(led, start, end)

    def step(self):
        for i in range(self._size):
            color = (i + self._step) % 384
            self._led.set(self._start + i, wheel_color(color))

        self._step += 1
        if self._step > 384:
            self._step = 0
        
        return True

            
class RainbowCycle(BaseAnimation):
    """Generate rainbow wheel equally distributed over strip."""

    def __init__(self, led, start=0, end=0):
        super(RainbowCycle, self).__init__(led, start, end)

    def step(self):
        for i in range(self._size):
            color = (i * (384 / self._size) + self._step) % 384
            self._led.set(self._start + i, wheel_color(color))

        self._step += 1
        if self._step > 384:
            self._step = 0
        
        return True

class ColorPattern(BaseAnimation):
    """Fill the dots progressively along the strip with alternating colors."""

    def __init__(self, led, colors, width, step_size = 1, dir = True, start=0, end=0):
        super(ColorPattern, self).__init__(led, start, end)
        self._colors = colors
        self._colorCount = len(colors)
        self._width = width
        self._step_size = step_size
        self._total_width = self._width * self._colorCount;
        self._dir = dir

    def step(self):
        for i in range(self._size):
            cIndex = ((i+self._step) % self._total_width) / self._width;
            self._led.set(self._start + i, self._colors[cIndex])
        if self._dir:
            self._step += self._step_size
            if self._start + self._step > self._end:
                self._step = 0
        else:
            self._step -= self._step_size
            if self._step < 0:
                self._step = self._end
                
        return True
                
class ColorWipe(BaseAnimation):
    """Fill the dots progressively along the strip."""

    def __init__(self, led, color, start=0, end=0):
        super(ColorWipe, self).__init__(led, start, end)
        self._color = color

    def step(self):
        if self._step == 0:
            self._led.fillOff()

        self._led.set(self._start + self._step, self._color)

        self._step += 1
        if self._start + self._step > self._end:
            self._step = 0
        
        return True

class ColorChase(BaseAnimation):
    """Chase one pixel down the strip."""

    def __init__(self, led, color, start=0, end=0):
        super(ColorChase, self).__init__(led, start, end)
        self._color = color

    def step(self):
        if self._step == 0:
            self._led.setOff(self._end)
        else:
            self._led.setOff(self._start + self._step - 1)

        self._led.set(self._start + self._step, self._color)

        self._step += 1
        if self._start + self._step > self._end:
            self._step = 0
        return True

class LarsonScanner(BaseAnimation):
    """Larson scanner (i.e. Cylon Eye or K.I.T.T.)."""

    def __init__(self, led, color, tail=2, fade=0.75, start=0, end=0):
        super(LarsonScanner, self).__init__(led, start, end)
        self._color = color

        self._tail = tail + 1  # makes tail math later easier
        if self._tail >= self._size / 2:
            self._tail = (self._size / 2) - 1

        self._fade = fade
        self._direction = -1
        self._last = 0

    def step(self):
        self._last = self._start + self._step
        self._led.set(self._last, self._color)

        tl = self._tail
        if self._last + tl > self._end:
            tl = self._end - self._last
        tr = self._tail
        if self._last - tr < self._start:
            tr = self._last - self._start

        for l in range(1, tl + 1):
            level = (float(self._tail - l) / float(self._tail)) * self._fade
            self._led.setRGB(self._last + l,
                             self._color.r * level,
                             self._color.g * level,
                             self._color.b * level)

        if self._last + tl + 1 <= self._end:
            self._led.setOff(self._last + tl + 1)

        for r in range(1, tr + 1):
            level = (float(self._tail - r) / float(self._tail)) * self._fade
            self._led.setRGB(self._last - r,
                             self._color.r * level,
                             self._color.g * level,
                             self._color.b * level)

        if self._last - tr - 1 >= self._start:
            self._led.setOff(self._last - tr - 1)

        if self._start + self._step == self._end:
            self._direction = -self._direction
        elif self._step == 0:
            self._direction = -self._direction

        self._step += self._direction
        
        return True


class LarsonRainbow(LarsonScanner):
    """Larson scanner (i.e. Cylon Eye or K.I.T.T.) but Rainbow."""

    def __init__(self, led, tail=2, fade=0.75, start=0, end=0):
        super(LarsonRainbow, self).__init__(
            led, ColorHSV(0).get_color_rgb(), tail, fade, start, end)

    def step(self):
        self._color = ColorHSV(self._step * (360 / self._size)).get_color_rgb()

        super(LarsonRainbow, self).step()
        return True

class Wave(BaseAnimation):
    """Sine wave animation."""

    def __init__(self, led, color, cycles, start=0, end=0):
        super(Wave, self).__init__(led, start, end)
        self._color = color
        self._cycles = cycles

    def step(self):
        for i in range(self._size):
            y = math.sin(
                math.pi *
                float(self._cycles) *
                float(self._step * i) /
                float(self._size))

            if y >= 0.0:
                # Peaks of sine wave are white
                y = 1.0 - y  # Translate Y to 0.0 (top) to 1.0 (center)
                c2 = Color(255 - float(255 - self._color.r) * y,
                           255 - float(255 - self._color.g) * y,
                           255 - float(255 - self._color.b) * y)
            else:
                # Troughs of sine wave are black
                y += 1.0  # Translate Y to 0.0 (bottom) to 1.0 (center)
                c2 = Color(float(self._color.r) * y,
                           float(self._color.g) * y,
                           float(self._color.b) * y)
            self._led.set(self._start + i, c2)

        self._step += 1
        
        return True
        
class Fade(BaseAnimation):
    """Fades from one color to another"""
    def __init__(self, led, current_color, end_color, fade_steps=1000, start=0, end=0):
        super(Fade, self.__init__(led, start, end)
        self._current_color = start_color
        self._end_color = end_color
        self._fade_steps = fade_steps
        
        self._r_step = (self._start_color.r - self._end_color.r)/self._fade_steps 
        self._g_step = (self._start_color.g - self._end_color.g)/self._fade_steps 
        self._b_step = (self._start_color.b - self._end_color.b)/self._fade_steps 
        

        
    def step(self):
        self._led.fillRGB(self._current_color, self._start, self._end)
        if (self._steps < self._fade_steps):
            #Increase to next increment in the color cycle
            self._current_color.r += self._r_step 
            self._current_color.g += self._g_step
            self._current_color.b += self._b_step
            self._step += 1
            return True
        else:
            return False