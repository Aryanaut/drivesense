import pynmea2
import time
import serial

class GPS:
    def __init__(self):
        global gps, line, lat, lon
        gps = serial.Serial("/dev/ttyACM1", baudrate = 9600)

    def readAndDecode(self):
        global lat, lon
        line = gps.readline()
        line = line.decode()
        data = line.split(",")
        if data[0] == "$GPRMC":
            msg = pynmea2.parse(line)
            lat = msg.latitude
            lat = str(lat)
            lon = msg.longitude
            lon = str(lon)

    def link(self):
        maps = "https://www.google.com/maps/place/"+lat+","+lon
        return(maps)
