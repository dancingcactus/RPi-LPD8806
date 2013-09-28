from LPD8806 import *
import Queue

queue = Queue.Queue(0)

queue.put(Color(255,0,0))
queue.put(Color(0,255,0))
queue.put(Color(0,0,255))
queue.put(Color(0,128,255))
queue.put(None)

leds = LEDStrip(30,queue)

leds.start()
print "LEDs Started";

leds.join();
