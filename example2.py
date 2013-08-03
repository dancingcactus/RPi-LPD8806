#!/usr/bin/python

from time import sleep
from LPD8806 import *

def setRow(r,g,b,rowNum):
	currentPixel = rowNum*6;
	led.fillRGB(r,g,b,currentPixel, currentPixel + 5);

def setColumn(r,g,b,colNum):
	currentPixel = colNum
	for i in range(5):
		led.setRGB(currentPixel,r,g,b);
		currentPixel +=6;
		print(currentPixel);

num = 30;
led = LEDStrip(num);
# Make sure I don't pull too much current
led.setMasterBrightness(0.7);

# Make sure everything is off
led.all_off();

for i in range(5):
	led.all_off();
	setRow(255,0,0,i);
	led.update();
	sleep(0.2);

led.all_off();

for i in range(6):
	led.all_off();
	setColumn(0,255,0,i);
	led.update();
	sleep(0.3);

led.all_off();
