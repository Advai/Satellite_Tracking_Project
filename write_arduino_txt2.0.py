
"""
import gps as gp
file_ = open("2_GPS_Bearing_test3_4short", "w")
gps1 = gp.GPS("COM4", 115200)
gps1.refresh()
if gps1.is_fixed():
    lat = gps1.get_lat()
    lon = gps1.get_lon()
    print (lat, lon)
    file_.write("%s %s\n" % (lat, lon))
else:
    print("Can't get fixed")"""
import time
import math
import gps as gp
def findHeading(lat, lon, lat2, lon2):
    y = lon2 - lon
    x = lat2 - lat
    return 90 - math.degrees(math.atan2(y, x))

g = gp.GPS("COM5", 115200)
f1 = open("GPS1_output", "w+")
f2 = open("GPS2_output", "w+")
f3 = open("Bearing", "w+")
while True:
    g.refresh()
    checkGPS = str(g.info[len(g.info)-1])
    lat = g.get_lat()
    lon = g.get_lon()
    time = g.get_time()
    if checkGPS[0:4] == "GPS1":
        f1.write("%s %s %s\n" % (lat, lon, time))
    elif checkGPS[0:4] == "GPS2":
        f2.write("%s %s %s\n" % (lat, lon, time))
    g.refresh()
    lat2 = g.get_lat()
    lon2 = g.get_lon()
    if (lat2-lat > 0.001 or lon2-lon > 0.001):
        print("Found Movement")
        f1.write("-----------------------------------")
        f2.write("-----------------------------------")
    bearing = findHeading(lat, lon, lat2, lon2)
    print(bearing)
    f3.write("%s\n" % bearing)
f1.close()
f2.close()
                 