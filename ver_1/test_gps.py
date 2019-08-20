from ds_gps import GPS

g = GPS()

while True:
    g.readAndDecode()
    a = g.link()
    print(a)