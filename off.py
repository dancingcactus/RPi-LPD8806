#!/usr/bin/python

from time import sleep
from LPD8806 import *

num = 48*5;
led = LEDStrip(num)
led.setChannelOrder(ChannelOrder.BRG)
led.all_off()


