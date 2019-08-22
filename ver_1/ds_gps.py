import pynmea2
import time
import serial

class GPS:
    def __init__(self):
        global gps
        gps = serial.Serial("/dev/ttyUSB0", baudrate = 9600)

    def readAndDecode(self):
        global lat, lon, lati, longi
        line = gps.readline()
        line = line.decode()
        data = line.split(",")
        if data[0] == "$GPRMC":
            msg = pynmea2.parse(line)
            lat = msg.latitude
            lati = str(lat)
            lon = msg.longitude
            longi = str(lon)

    def link(self):
        maps = "https://www.google.com/maps/place/"+lati+","+longi
        return(maps)
