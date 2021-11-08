#!/usr/bin/env python3
# From: https://github.com/blynkkk/lib-python
import blynklib
import os, sys
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.SPI as SPI
import Adafruit_MAX31855.MAX31855 as MAX31855

# Set up pins for PowerSwitch Tail 2
Switch = 'P9_14'
GPIO.setup(Switch, GPIO.OUT)
GPIO.output(Switch, 1)

# Set up the Pins for SPI
CLK = 'P9_12'
CS  = 'P9_15'
DO  = 'P9_23'
sensor = MAX31855.MAX31855(CLK, CS, DO)

# Create variables
On = 1
CurrentTemp = int(sensor.readTempC())
start = True
Goal = 0
GoalHolder = 0
GoalPrev = 0
PrevTemp = 0
count = 50
degree_sign = u"\N{DEGREE SIGN}"

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
    global On
    if(int(value[0]) == 0):
        On = 1
        print("Turning power off")
    if(int(value[0]) == 1):
        On = 0
        print("Turning power on")
    GPIO.output(Switch, int(On))
    
#quit the program
@blynk.handle_event('write V1')
def my_write_handler2(pin, value):
    print('\nClosing the app')
    GPIO.output(Switch, 1)
    exit()
    
#read the current temperature
@blynk.handle_event('read V2')
def my_read_handler(pin):
    blynk.virtual_write(2, CurrentTemp)
    
# Hold the temporary value set by the numerical input module
@blynk.handle_event('write V3')
def my_write_handler3(pin, value):
    global GoalHolder
    GoalHolder = int(value[0])
    
# Set the primary goal temp to the temporary one
@blynk.handle_event('write V4')
def my_write_handler4(pin, value):
    if (int(value[0]) == 1):
        global Goal 
        Goal = GoalHolder
    
while True:
    # Run the blynk client. Needs to be run every update
    blynk.run()
    
    # Set the message template and current temperature and reprint every 50 updates
    if (count >= 10):
        CurrentTemp = int(sensor.readTempC())
        message = "Current Temp: {}{}C  Goal Temp: {}{}C".format(CurrentTemp,degree_sign,Goal,degree_sign)
        print(message,end="\r") # Print the message on the same line
        count = 0
    count = count + 1
    
    
# had to install the MAX31855 library
# use tmux for long term testing