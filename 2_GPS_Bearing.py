import math
import gps as gp

def findHeading(lat, lon, lat2, lon2):
    y = lon - lon2
    x = lat - lat2
    bearing = 90 - math.degrees(math.atan2(y, x))
    if(bearing<0):
        return bearing+360
    else:
        return bearing
file1 = open("GPS1_4GPS_test2.txt", "r")
file2 = open("GPS3_4GPS_test2.txt", "r")
file3 = open("4GPS_bearing_comparison.txt", "w")
for line in file1:
    try:
        myArr = file1.readline().split(" ")
        nextPair = file2.readline().split(" ")
        lat = float(myArr[0])
        lon = float(myArr[1])
        lat2 = float(nextPair[0])
        lon2 = float(nextPair[1])
        
        print(findHeading(lat,lon,lat2,lon2))
        result = findHeading(lat, lon, lat2, lon2)
        file3.write("%s\n" % result)        
    except ValueError:
        print("RIP")
        file3.close()
        break
