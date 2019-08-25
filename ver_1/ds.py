"""
    ds.py
    Author: Aryan Mahesh

    Description: main code for driveSense

"""
from ds_accel import ADXL
from ds_gps import GPS
from ds_cv2 import cv
from ds_sms import sms
import cv2
gps = GPS()
cv = cv()

cv.drowsinessDetect()