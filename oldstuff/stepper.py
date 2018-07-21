
import RPi.GPIO as GPIO
import time

import sys

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
def step( direction, count ):
	GPIO.output(23, direction)
	for x in range(count):
		GPIO.output(24, False)
		GPIO.output(24, True)
		time.sleep(float(sys.argv[1]))
while True:
	step ( False, int(sys.argv[2]))
	time.sleep(float(sys.argv[3])) 
	
#	step ( True, int(sys.argv[2]))
#	time.sleep(2)
print "Done..."
