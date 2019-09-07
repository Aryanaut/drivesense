"""
	read-test.py

	Description:

	...

	Author: Aryan Mahesh
	Website: aryanaut.wordpress.com

"""

import smbus
import RPi.GPIO as gpio
import time
import ctypes

# address and regsiters
DEV_ADDR 		= 0x53
INT_ENABLE 		= 0x2E
INT_MAP 		= 0x2F
THRESH_ACT		= 0x24
ACT_INACT_CTL 	= 0x27

def accel_cb(channel):  
    print("crash alert at chan = %d\n" % (channel,)) 

# Main function
def main():

	bus = smbus.SMBus(1)
	print("initalising byte reading...")

	gpio.setmode(gpio.BCM)

	INT_PIN_2 = 24
	gpio.setup(INT_PIN_2, gpio.IN)
	# read device ID
	DID = bus.read_byte_data(DEV_ADDR, 0x00)
	print("DID = 0x%2x\n" % (DID, ))

	# set power ctrl
	bus.write_byte_data(DEV_ADDR, 0x2D, 0x08)

	# setup
	bus.write_byte_data(DEV_ADDR, INT_ENABLE, 0x90) #enables interrupt
	bus.write_byte_data(DEV_ADDR, INT_MAP, 0x90) #maps interrupts to INT_PIN2
	bus.write_byte_data(DEV_ADDR, THRESH_ACT, 0x15) #threshold
	bus.write_byte_data(DEV_ADDR, ACT_INACT_CTL, 0x70) #setting the x, y, z axis to participate in the interrupt detection

	a = bus.read_byte_data(DEV_ADDR, 0x2e)
	b = bus.read_byte_data(DEV_ADDR, 0x2f)
	c = bus.read_byte_data(DEV_ADDR, 0x24)
	d = bus.read_byte_data(DEV_ADDR, 0x27)
	print("int_enable", bin(a))
	print("map", bin(b))
	print("threshold", bin(c))
	print("actinact_ctl", bin(d))
	
	# set up accel interrupt
	gpio.add_event_detect(24, gpio.RISING, callback=accel_cb)

	while True:
		state = gpio.input(INT_PIN_2)
		vals = bus.read_i2c_block_data(DEV_ADDR, 0x32, 6)
		#x = ctypes.c_int16(vals[0] | vals[1] << 8).value
		#y = ctypes.c_int16(vals[2] | vals[3] << 8).value
		#z = ctypes.c_int16(vals[4] | vals[5] << 8).value
		#print(x, y, z, state)


# call main
if __name__ == '__main__':
    main()
