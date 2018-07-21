#!/usr/bin/python
#The following script uses port 11 and executes the shutter release.

#Port 6 is Ground
#Port 11 is Live

#Imports the GPIO Library
import RPi.GPIO as GPIO

#Enables Time / Pause
import time
import signal
import sys
import os
import daemon.pidfile
import daemon



focusPort=18
shutterPort=16
shutter_speed=0.1
period=4
shutter_count=-1
focusTime=0

pid = "/tmp/shutter.pid"


def cleanup():
    global focusPort
    global shutterPort
    print("resetting GPIO")
    GPIO.output(focusPort,False)
    GPIO.output(shutterPort,False)

def catcher(signum, _):
    global shutter_speed
    global focusTime  
    global focusPort
    global shutterPort
    print("focus")
    GPIO.output(focusPort, True)
    if (focusTime>0):
      time.sleep(focusTime)
    print("shutter")
    GPIO.output(shutterPort, True)

    time.sleep(shutter_speed)

    print("release")
    GPIO.output(shutterPort, False)
    GPIO.output(focusPort, False)

    global shutter_count
    if shutter_count>0:
      print(shutter_count)
      shutter_count -= 1
    if shutter_count==0:
      cleanup()
      sys.exit()
    
def main():
  global shutter_speed
  global shutter_count
  global period
  global focusPort
  global shutterPort

  signal.signal(signal.SIGALRM, catcher)

  if len(sys.argv)<3:
    print("usage: "+sys.argv[0] + " <period> <shutter speed in s> [shutter count]")
  #  GPIO.cleanup()
    sys.exit()

  #Set the Board Mode
  GPIO.setmode(GPIO.BOARD)

  #Sets up GPIO Pin 11 to Output
  GPIO.setup(focusPort, GPIO.OUT)
  GPIO.setup(shutterPort, GPIO.OUT)

  GPIO.output(shutterPort, False)
  GPIO.output(focusPort, False)

  period = float(sys.argv[1])
  focusTime=0
  if (period>5):
    # after around 7 seconds the camera goes to sleep. we need a "focus" trigger to wake it up. we will just use 2 seconds for that
    focusTime=2


  shutter_speed = float(sys.argv[2])

  if (len(sys.argv))>3:
    shutter_count=int(sys.argv[3])

  if (shutter_speed>=(period-0.1)):
    sys.exit()

  print("period: ", period, "shutter: ", shutter_speed, "shutter_count: ", shutter_count)
  sys.stdout.flush()


  signal.setitimer(signal.ITIMER_REAL, 0.1, period)

  try:
    while True:
        time.sleep(5)
  finally:
    cleanup()


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    out = open('/tmp/shutter.log', 'w+')
    err = open('/tmp/shutter.err', 'w+')

    with daemon.DaemonContext(working_directory=here,stdout=out,stderr=err,pidfile=daemon.pidfile.PIDLockFile(pid)):
      main()


