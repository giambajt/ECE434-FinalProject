#!/usr/bin/python

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.SPI as SPI
import Adafruit_MAX31855.MAX31855 as MAX31855

CLK = 'P9_12'
CS = 'P9_15'
DO = 'P9_23'
sensor = MAX31855.MAX31855(CLK, CS, DO)
CurrentTemp = int(sensor.readTempC())
print(str(CurrentTemp))

