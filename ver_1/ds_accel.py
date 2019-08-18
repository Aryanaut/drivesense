"""
    ds_accel.py
    Description: Code for controlling ADXL345 accelerometer
    Author: Aryan Mahesh
"""
import smbus
import RPi.GPIO as gpio
import time 
import ctypes

class ADXL:
    global DEV_ADDR, INT_ENABLE, INT_MAP, THRESH_ACT, ACT_INACT_CTL, bus
    DEV_ADDR 		= 0x53
    INT_ENABLE 		= 0x2E
    INT_MAP 		= 0x2F
    THRESH_ACT		= 0x24
    ACT_INACT_CTL 	= 0x27

    bus = smbus.SMBus(1)
    
    def __init__(self):
        print("Initialising...")
        DID = bus.read_byte_data(DEV_ADDR, 0x00)
        print("DID = 0x%2x\n" % (DID, ))
        bus.write_byte_data(DEV_ADDR, 0x2D, 0x08)
        gpio.setmode(gpio.BCM)
        gpio.setup(24, gpio.OUT)

    def accel_cb():
        return True

    def readData():
        vals = bus.read_i2c_block_data(DEV_ADDR, 0x32, 6)
        x = ctypes.c_int16(vals[0] | vals[1] << 8).value
        y = ctypes.c_int16(vals[2] | vals[3] << 8).value
        z = ctypes.c_int16(vals[4] | vals[5] << 8).value
        return(x, y, z)

    def intRead():
        bus.write_byte_data(DEV_ADDR, INT_ENABLE, 0x90) #enables interrupt
        bus.write_byte_data(DEV_ADDR, INT_MAP, 0x90) #maps interrupts to INT_PIN2
        bus.write_byte_data(DEV_ADDR, THRESH_ACT, 0x15) #threshold
        bus.write_byte_data(DEV_ADDR, ACT_INACT_CTL, 0x70) #setting the x, y, z axis to participate in the interrupt detection
        
        gpio.add_event_detect(24, gpio.RISING, callback=accel_cb)