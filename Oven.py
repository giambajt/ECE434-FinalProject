#!/usr/bin/env python3
# From: https://github.com/blynkkk/lib-python
import blynklib
import os, sys
import Adafruit_BBIO.GPIO as GPIO
from simple_pid import PID

pid = PID(1, 0.1, 0.05, setpoint=1)
pid.sample_time = 1

LED = 'P9_14'
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, 1) 

button = 'P9_11'
GPIO.setup(button, GPIO.IN)

On = 1
tempCurrent = 1000
tempGoal = 0
start = True
outputPrev = 0.0

# Get the autherization code (See setup.sh)
# BLYNK_AUTH = os.getenv('BLYNK_AUTH', default="")
BLYNK_AUTH = "6odi1LyVWuqKuQqFzXOQDHXg_hXqbKar"
if(BLYNK_AUTH == ""):
    print("BLYNK_AUTH is not set")
    sys.exit()

# Initialize Blynk
blynk = blynklib.Blynk(BLYNK_AUTH)

#turn the powerswitch on/off
@blynk.handle_event('write V0')
def my_write_handler(pin, value):
    if(int(value[0]) == 0):
        On = 1
        print("Turning power off")
    if(int(value[0]) == 1):
        On = 0
        print("Turning power on")
    GPIO.output(LED, int(On))
    
#quit the program
@blynk.handle_event('write V1')
def my_write_handler2(pin, value):
    print('Closing the app')
    GPIO.output(LED, 1)
    exit()
    
#read the current temperature
@blynk.handle_event('read V2')
def my_read_handler(pin):
    print("ping")
    i = GPIO.input(button)
    blynk.virtual_write(2, 1100)
    
#set the desired temperature
@blynk.handle_event('write V3')
def my_write_handler3(pin, value):
    # tempGoal = value
    pid.setpoint = int(value[0])
    print("Temperature set to: {}".format(value[0]))
    
while True:
    blynk.run()
    if(start):
        blynk.virtual_write(3, 0)
        start = False
    #tempCurrent = tempCurrent + 1
    output = pid(tempCurrent)
    if (output != outputPrev):
        print(output)
    outputPrev = output
    
    #output is all about the difference in values produced by the pid
    #if there is a difference between two values of 10 or more then it should be on constantly
    #if there is a difference of -10  or less then it should be off constantly 
    #if there is a difference of 0 then it should be on and off for equal amounts of time