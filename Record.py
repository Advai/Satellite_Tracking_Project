from datetime import datetime

class Record:

    def __init__(self, lati, loni, timei):
        self.latitude = float(lati)
        self.longitude = float(loni)
        self.time = timei
    def getString(self):
        return (str(self.latitude) + "," + str(self.longitude) + "," + str(self.time)+"\n")

def extrapolate (storage, ptime):

    n = len(storage) * 1.0
    xbar, x2bar, lonbar, xlonbar, latbar, xlatbar = 0, 0, 0, 0, 0, 0
    for record in storage:

        time = datetime.strptime(record.time.split(".")[0], "%H:%M:%S")
        x = 3600 * time.hour + 60 * time.minute + time.second
        xbar += x
        x2bar += x * x
        lonbar += record.longitude
        xlonbar += x * record.longitude
        latbar += record.latitude
        xlatbar += x * record.latitude

    xbar /= n
    x2bar /= n
    lonbar /= n
    xlonbar /= n
    latbar /= n
    xlatbar /= n

    stdev = x2bar - xbar * xbar
    stdevlon = xlonbar - xbar * lonbar
    stdevlat = xlatbar - xbar * latbar
    betalon = stdevlon / stdev
    betalat = stdevlat / stdev
    alphalon = lonbar - betalon * xbar
    alphalat = latbar - betalat * xbar

    ptimed = datetime.strptime(ptime.split(".")[0], "%H:%M:%S")
    ptimex = 3600 * ptimed.hour + 60 * ptimed.minute + ptimed.second
    newlon = alphalon + betalon * ptimex
    newlat = alphalat + betalat * ptimex

    record = Record(newlat, newlon, ptime)
    return record


"""
def interpolate (prev1, prev2, prev3, prev4, curr1, curr2, curr3, curr4):

    velo_lat1 = getVelo(curr1.latitude, prev1.latitude, curr1.time, prev1.time)
    velo_lon1 = getVelo(curr1.longitude, prev1.longitude, curr1.time, prev1.time)
    velo_lat2 = getVelo(curr1.latitude, prev1.latitude, curr2.time, prev2.time)
    velo_lon2 = getVelo(curr1.longitude, prev1.longitude, curr2.time, prev2.time)
    velo_lat3 = getVelo(curr1.latitude, prev1.latitude, curr3.time, prev3.time)
    velo_lon3 = getVelo(curr1.longitude, prev1.longitude, curr3.time, prev3.time)
    velo_lat4 = getVelo(curr1.latitude, prev1.latitude, curr4.time, prev4.time)
    velo_lon4 = getVelo(curr1.longitude, prev1.longitude, curr4.time, prev4.time)

    propertime = min( min(curr1.time, curr2.time), min(curr3.time, curr4.time) )

    new_lat1 = getLat(prev1.latitude, propertime, prev1.time, velo_lat1)
    new_lon1 = getLat(prev1.longitude, propertime, prev1.time, velo_lon1)
    new_lat2 = getLat(prev2.latitude, propertime, prev2.time, velo_lat2)
    new_lon2 = getLat(prev2.longitude, propertime, prev2.time, velo_lon2)
    new_lat3 = getLat(prev3.latitude, propertime, prev3.time, velo_lat3)
    new_lon3 = getLat(prev3.longitude, propertime, prev3.time, velo_lon3)
    new_lat4 = getLat(prev4.latitude, propertime, prev4.time, velo_lat4)
    new_lon4 = getLat(prev4.longitude, propertime, prev4.time, velo_lon4)

    new1 = Record(new_lat1, new_lon1, propertime)
    new2 = Record(new_lat2, new_lon2, propertime)
    new3 = Record(new_lat3, new_lon3, propertime)
    new4 = Record(new_lat4, new_lon4, propertime)

    return new1, new2, new3, new4


def getVelo (y2, y1, x2, x1):
    time2 = datetime.strptime(x2.split(".")[0], "%H:%M:%S")
    time1 = datetime.strptime(x1.split(".")[0], "%H:%M:%S")
    timedif = time2 - time1
    return (float(y2) - float(y1)) / timedif.seconds

def getLat (y0, x2, x1, velo):
    time2 = datetime.strptime(x2.split(".")[0], "%H:%M:%S")
    time1 = datetime.strptime(x1.split(".")[0], "%H:%M:%S")
    timedif = time2 - time1
    return float(y0) + timedif.seconds * float(velo)
"""