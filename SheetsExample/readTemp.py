#!/usr/bin/python

import smbus

tmp = smbus.SMBus(1)

addr = 0x49
output = tmp.read_byte_data(addr, 0)
print(str((output*1.8) +32))

