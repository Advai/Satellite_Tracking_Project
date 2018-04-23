import math
import gps as gp
# class myThread(threading.Thread):
#     def __init__(self):
#         threading.Thread.__init__(self)
#
#     def run(self):
#         global val
#         global ii
#         val = '@'
#         ii = ''
#         while True:
#             ii = input()
#             if ii == 'q':
#                 break
#             val = chr(ord(val)+1)
#             pass


def gps12latlon():
    with open("GPS1_4GPS_test1.txt", "w") as f1:
        with open("GPS2_4GPS_test1.txt", "w") as f2:
            initVal = [0, 0, 0, 0, 0, 0]
            try:
                for i in range(2):
                    gps12.refresh()
                    checkGPS = str(gps12.info[len(gps12.info) - 1])
                    if gps12.is_fixed():
                        lat = str(gps12.get_lat())
                        lon = str(gps12.get_lon())
                        time = str(gps12.get_time())
                        if checkGPS[0:4] == "GPS1":
                            f1.write("%s %s %s\n" % (lat, lon, time))
                            initVal[0] = float(lat)
                            initVal[1] = float(lon)
                            initVal[4] = time
                        elif checkGPS[0:4] == "GPS2":
                            f2.write("%s %s %s\n" % (lat, lon, time))
                            initVal[2] = float(lat)
                            initVal[3] = float(lon)
                            initVal[5] = time
            except KeyboardInterrupt:
                print("Loop interrupted")
            if 0 in initVal:
                return None
            elif initVal[5] != initVal[4]:
                return None
            else:
                return initVal


def gps34latlon():
    with open("GPS3_4GPS_test1.txt", "w") as f1:
        with open("GPS4_4GPS_test1.txt", "w") as f2:
            initVal2 = [0, 0, 0, 0, 0, 0]
            try:
                for i in range(2):
                    gps34.refresh()
                    checkGPS = str(gps34.info[len(gps34.info) - 1])
                    if gps34.is_fixed():
                        lat = str(gps34.get_lat())
                        lon = str(gps34.get_lon())
                        time = str(gps34.get_time())
                        if checkGPS[0:4] == "GPS3":
                            f1.write("%s %s %s\n" % (lat, lon, time))
                            initVal2[0] = float(lat)
                            initVal2[1] = float(lon)
                            initVal2[4] = time
                        elif checkGPS[0:4] == "GPS4":
                            f2.write("%s %s %s\n" % (lat, lon, time))
                            initVal2[2] = float(lat)
                            initVal2[3] = float(lon)
                            initVal2[5] = time
            except KeyboardInterrupt:
                print("Loop interrupted")
            if 0 in initVal2:
                return None
            elif initVal2[5] != initVal2[4]:
                return None
            else:
                return initVal2


def setPolygon(coordinates):
    xcoord = (coordinates[1].x + coordinates[3].x) / 2
    ycoord = (coordinates[0].y + coordinates[2].y) / 2
    poly = Polygon(len(coordinates), Coordinate(xcoord, ycoord))
    poly.positions = coordinates
    return poly

def construct_polygon(self, centeri, ni, distance_radius=None):
    poly = Polygon(ni, centeri)
    poly.positions = []
    fullCircle = 360
    poly.curr = Vector(Coordinate(0, 0), poly.center)
    poly.positions.append(poly.curr.head)
    for i in range(1, int(poly.n)):
        toputin = fullCircle / poly.n
        poly.curr.rotate(toputin)
        poly.positions.append(poly.curr.head)
    return poly

def change(angle, iftodeg):
    multiplier = 180/math.pi
    if iftodeg:
        return angle*multiplier
    else:
        return angle/multiplier


class Coordinate:
    def __init__(self, x=0, y=0):
        self.x = float(x)
        self.y = float(y)

    def move(self, deltx, delty):
        self.x = float(self.x) + deltx
        self.y = float(self.y) + delty

    def movey(self, delty):
        self.y += float(self.y) + delty
        return self.y

class Vector:
    def __init__(self, headi, taili):
        self.head = headi
        self.tail = taili

    def vecAngle(self):
        return math.atan2(self.head.y - self.tail.y, self.head.x - self.tail.x) - math.pi/2

    def distance(self):
        dist = (self.head.x - self.tail.x) * (self.head.x - self.tail.x)
        dist += (self.head.y - self.tail.y) * (self.head.y - self.tail.y)
        return dist

    def getHeading(self):
        angRadians = self.vecAngle()
        full_circle = math.pi * 2
        if angRadians < 0:
            angRadians += full_circle
        return change(angRadians, True)

    def rotate(self, angle):
        angle = change(angle, False)
        rot = self.head
        rot.move(-1*self.tail.x, -1*self.tail.y)
        newx = rot.x * math.cos(angle) - rot.y * math.sin(angle)
        newy = rot.x * math.sin(angle) + rot.y * math.cos(angle)
        self.head = Coordinate(newx, newy)
        self.head.move(self.tail.x, self.tail.y)
        return self.head.x, self.head.y


class Polygon:
    def __init__(self, input, centeri): #centeri is a coordinate object
         self.positions = [None for i in range(input)]
         self.n = input
         self.center = centeri


    def rotate(self, angle):
        newpos = [0 for i in range(self.n)]
        for i in range(round(self.n, 0)):
            vec = Vector(self.positions[i], self.center)
            vec.rotate(angle)
            newpos[i] = vec.head
        self.positions = newpos

    def shift(self, shifts):
        self.poly = Polygon(self.center, self.n)
        self.newpos = []
        for i in range(round(self.n),0):
            self.poly.positions[i] = self.positions[i]
            self.poly.positions[i].move(shifts[2*i], shifts[2*i+1])
        poly = self.poly
        return poly


    def difference(self, s2):
        diff = 0
        for i in range(round(self.n), 0):
            vec = Vector(self.positions[i], s2.positions[i])
            diff += vec.distance()
        return diff

    def getheading(self):
        north = Vector(self.positions[0], self.center)
        return north.getHeading()

    def box(self):
        farleft, fartop, farright, farbot = 0,0,0,0
        for i in range(round(self.n, 0)):
            if self.positions[i].x < farleft:
                farleft = self.positions[i].x
            if self.positions[i].x > farright:
                farright = self.positions[i].x
            if self.positions[i].y < farbot:
                farbot = self.positions[i].y
            if self.positions[i].y > fartop:
                fartop = self.positions[i].y
        xdist = farright - farleft
        ydist = fartop - farbot
        farleft += xdist/ 4.0
        farright -= xdist /4.0
        farbot += ydist /4.0
        fartop -= ydist/4.0
        head = Coordinate(farright, fartop)
        tail = Coordinate(farleft, farbot)
        return Vector(head, tail)

    def bestpoly(self, distanceRadius):
        nothing = Coordinate()
        bestsim = Polygon(0,nothing)
        currsim = Polygon(0, nothing)
        minerror = 10000
        fullcircle, arcdeg, acccen = 360, .5, .05
        boxx = self.box()
        x = boxx.tail.x
        y = boxx.tail.y
        while x < boxx.head.x:
            while y < boxx.head.y:
                center = Coordinate(x,y)
                currsim = construct_polygon(distanceRadius, center, self.n)
                currsim.rotate(-fullcircle / (2*self.n))
                i = 0
                while(i < fullcircle / (arcdeg* self.n)):
                    if self.difference(currsim) < minerror:
                        minerror = self.difference(currsim)
                        bestsim = currsim
                    currsim.rotate(arcdeg)
                    i += 1
                y += acccen
            x += acccen
        return bestsim
# testCo = Coordinate(41.78770667, -88.35622)
# testCo2 = Coordinate(41.78770667, -88.35624167)
# Vec = Vector(Coordinate(41.78770667, -88.35624167), Coordinate(41.78770667, -88.35622))
# vec2 = Vector(testCo, testCo2)
# poly = Polygon(Coordinate(41.78770667, -88.35624167), .5, 2)
# shifts = [0, 1, 2, 3, 4, 5]
# print(poly.shift(shifts))
# GPS = Polygon()
f = open("Bearing_4GPS_test1", "w")
distanceRadius = 1.25
gps13 = gp.GPS("COM4", 115200)
gps24 = gp.GPS("COM3", 115200)
# f1 = open("GPS1_4GPS_test3.txt", "r+")
# f2 = open("GPS2_4GPS_test3.txt", "r+")
# f3 = open("GPS3_4GPS_test3.txt", "r+")
# f4 = open("GPS4_4GPS_test3.txt", "r+")
#
# thread1 = myThread()
#
# thread1.start()

with open("GPS1_4GPS_test4.txt", "r+") as f1:
    with open("GPS2_4GPS_test4.txt", "r+") as f2:
        with open("GPS3_4GPS_test4.txt", "r+") as f3:
            with open("GPS4_4GPS_test4.txt", "r+") as f4:
                while True:
                    arr1 = gps13.gps1234latlon(f1, f3, "GPS1", "GPS3")
                    arr2 = gps24.gps1234latlon(f2,f4, "GPS2", "GPS4")
                    if arr1 is None or arr2 is None:
                        print("fail")
                        print(arr1, arr2)
                        continue
                    else:
                        # if arr1[5] != arr2[5]:
                        print("pass")
                        # coordinates = [Coordinate(arr1[0], arr1[1]), Coordinate(arr2[0], arr2[1]), Coordinate(arr1[2], arr1[3]), Coordinate(arr2[2], arr2[3])]
                        # poly = setPolygon(coordinates)
                        # heading = (poly.bestpoly(distanceRadius)).getheading()
                        # f.write(str(heading))
                        # print(heading)
