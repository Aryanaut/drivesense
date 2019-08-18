from ds_accel import ADXL
from ds_sms import sms
from ds_gps import GPS
import time

a = ADXL()
g = GPS
while True:
    g.readAndDecode()
    lnk = g.link()
    if a.check_evt():
        sms.sendMSG('+919449018825', lnk)
        print("OK")
        

