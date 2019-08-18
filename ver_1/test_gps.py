from ds_gps import GPS

g = GPS()

while True:
    g.readAndDecode()
    g.link()