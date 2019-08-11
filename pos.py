import pynmea2
import time
import serial
gps = serial.Serial("/dev/ttyACM1", baudrate = 9600)

while True:
        line = gps.readline()
        line = line.decode()
        data = line.split(",")
        if data[0] == "$GPRMC":
                msg = pynmea2.parse("$GPRMC,054758.00,A,1256.30860,N,07735.16396,E,0.281,,110819,,,A*70")
                lat = msg.latitude
                lat = str(lat)
                long = msg.longitude
                long = str(long)
                print("https://www.google.com/maps/place/"+lat+","+long)
                time.sleep(3)

