#!/usr/bin/python

from time import sleep
from random import randrange
from LPD8806 import *


num = 30;
led = LEDStrip(num);
# Make sure I don't pull too much current
#led.setMasterBrightness(0.7);
led.enableGrid(5);
# Make sure everything is off
led.all_off();
'''
for i in range(5):
	led.all_off();
	led.setRowRGB(255,0,0,i);
	led.update();
	sleep(0.1);

led.all_off();

for i in range(6):
	led.all_off();
	led.setColumnRGB(0,255,0,i);
	led.update();
	sleep(0.1);

led.all_off();

#Fade
H = 0;
S = 1;
V = 1;

led.fillHSV(H,S,V);
led.update();

refresh = 0.5;

for i in range(100):
	V = V - 0.1;
	print S, V
	led.fillHSV(H,S,V);
	led.update();
	sleep(refresh);

sleep(1);
led.all_off();

#Fade RGB
fade = 1

R = 255;
G = 20;
B = 47;

for i in range(100):
	led.fillRGB((R*fade),(G*fade),(B*fade));
	led.update();
	print (R*fade)
	fade = fade - 0.01;
	sleep(0.01);

fade = 0.01;

for i in range(99):
	led.fillRGB((R*fade),(G*fade),(B*fade));
	led.update()
	fade = fade + 0.01;
	sleep(0.01);
sleep(1);
led.all_off();

#fade to another color
R1 = 255;
G1 = 20;
B1 = 147;

R2 = 64;
G2 = 224;
B2 = 208;

fade = 0.01;

led.fillRGB(R1,G1,B1);
sleep(1)
for i in range (360):
	print "New Color (R="+str(R2)+",G="+str(G2)+",B="+str(B2)+")"
	for i in range(100):
		if fade > 0 and fade <= 1:
			#print (R2-R1)*fade + R1
			led.fillRGB(((R2-R1)*fade + R1),((G2-G1)*fade + G1),((B2-B1)*fade + B1))
			led.update();
			fade = fade + 0.01;
			sleep(0.01);

	led.fillRGB(R2,G2,B2);
	sleep(1);
	#move the fade to color to the start color
	R1 = R2;
	G1 = G2;
	B1 = B2;
	
	#Gerenate a new color
	R2 = randrange(255);
	G2 = randrange(255);
	B2 = randrange(255);


	#reset fade
	fade = 0.01

led.all_off();
'''
R1 = 255;
G1 = 255;
B1 = 255;
fade = 0.1;


R2 = randrange(255);
G2 = randrange(255);
B2 = randrange(255);

for i in range (200):
	row =math.fabs((i%10)-5)
	rowBlank =math.fabs(((i-1)%10)-5)

	if row != 0: 
		#print row
		#print rowBlank

		fade = fade + 0.18
		if fade > 1:
			fade = 0.1;
			R1 = R2;
			G1 = G2;
			B1 = B2;

			R2 = randrange(255);
			G2 = randrange(255);
			B2 = randrange(255);
		
		print str(fade) +"-"+str(i%5)
		#led.setColumnRGB(0,0,0,(i-1)%5);
		#led.setColumnRGB(0,0,255,i%5)
		led.setRowRGB(((R2-R1)*fade + R1),((G2-G1)*fade+G1),((B2-B1)*fade+B1),int(row));
		led.setRowRGB(0,0,0,int(rowBlank));
		led.update();
		sleep(0.1);

led.all_off();
