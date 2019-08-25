from ver_1.ds_accel import ADXL
from ver_1.ds_sms import sms
from ver_1.ds_gps import GPS
import time

a = ADXL()
g = GPS()

while True:
    g.readAndDecode()
    lnk = g.link()
    if a.check_evt():
        sms.sendMSG('+919036430733', lnk)
        sms.sendWhatsapp('whatsapp:+919036430733', lnk)
        print("OK")

        

