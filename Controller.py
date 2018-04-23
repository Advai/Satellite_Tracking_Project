from time import time
import subprocess
import gps as gp
from time import time
import Record as record

supposedToInterpolate = True
f = "GPS1NCT2.txt"
file2 = "GPS2NCT2.txt"
file3 = "GPS3NCT2.txt"
file4 = "GPS4NCT2.txt"
heading_file = "CalibrationTest4.csv"
inRealTime = False
windowSize = 10

# change above

#just to make sure that we do not accidentally overwrite a heading file
print("the file that we will write to is: " + heading_file)
input("Are you sure you want to run?")

oldRecords1, oldRecords2, oldRecords3, oldRecords4 = [], [], [], []

if not inRealTime:
    with open(f) as f1:
        for line in f1:
            #print(line)
            l = line.split(' ')
            rec = record.Record(l[0], l[1], l[2])
            oldRecords1.append(rec)
    with open(file2) as f2:
        for line in f2:
            l = line.split(' ')
            rec = record.Record(l[0], l[1], l[2])
            oldRecords2.append(rec)
    with open(file3) as f3:
        for line in f3:
            l = line.split(' ')
            rec = record.Record(l[0], l[1], l[2])
            oldRecords3.append(rec)
    with open(file4) as f4:
        for line in f4:
            l = line.split(' ')
            rec = record.Record(l[0], l[1], l[2])
            oldRecords4.append(rec)

gps1 = gp.GPS(oldRecords1, inRealTime, "COM9", 115200)
gps2 = gp.GPS(oldRecords2, inRealTime, "COM7", 115200)
gps3 = gp.GPS(oldRecords3, inRealTime, "COM10", 115200)
gps4 = gp.GPS(oldRecords4, inRealTime, "COM8", 115200)

#shouldInterpolate = None

prevheading = 0

recordStorage1, recordStorage2, recordStorage3, recordStorage4 = [], [], [], []

with open(f, 'r') as f1:
    with open(file2, 'r') as f2:
        with open(file3, 'r') as f3:
            with open(file4, 'r') as f4:
                ifFirst = True
                of1x, of2x, of3x, of4x = 0,0,0,0
                of1y, of2y, of3y, of4y = 0,0,0,0
                while gps1.stillProcessing() and gps2.stillProcessing() and gps3.stillProcessing() and gps4.stillProcessing():
                    rec1 = gps1.getRecord()
                    rec2 = gps2.getRecord()
                    rec3 = gps3.getRecord()
                    rec4 = gps4.getRecord()

                    if (ifFirst):
                        of1x = rec1.latitude - 41.7864226666666664
                        of1y = rec1.longitude - -88.35629166666666
                        of2x = rec2.latitude - 41.786426666666664
                        of2y = rec2.longitude - -88.3562639982
                        of3x = rec3.latitude - 41.7864543
                        of3y = rec3.longitude - -88.356291666666666
                        of4x = rec4.latitude - 41.7864543
                        of4y = rec4.longitude - -88.3562639982


                    else:
                        rec1.latitude += of1x
                        rec1.longitude += of1y
                        rec2.latitude += of2x
                        rec2.longitude += of2y
                        rec3.latitude += of3x
                        rec3.longitude += of3y
                        rec4.latitude += of4x
                        rec4.longitude += of4y

                    if inRealTime:
                        f1.write(rec1.getString())
                        f2.write(rec2.getString())
                        f3.write(rec3.getString())
                        f4.write(rec4.getString())

                    if rec1 is None or rec2 is None or rec3 is None or rec4 is None:
                        #print("fail")
                        continue

                    #irec1, irec2, irec3, irec4 = rec1, rec2, rec3, rec4

                    recordStorage1.insert(0, rec1)
                    recordStorage2.insert(0, rec2)
                    recordStorage3.insert(0, rec3)
                    recordStorage4.insert(0, rec4)

                    if len(recordStorage1) > windowSize:
                        recordStorage1.pop()
                        recordStorage2.pop()
                        recordStorage3.pop()
                        recordStorage4.pop()

                    # find some time to use (earliest time?)
                    propertime = min(rec1.time, rec2.time, rec3.time, rec4.time)

                    irec1, irec2, irec3, irec4 = rec1, rec2, rec3, rec4
                    if len(recordStorage1) == windowSize:
                        irec1 = record.extrapolate(recordStorage1, propertime)
                        irec2 = record.extrapolate(recordStorage2, propertime)
                        irec3 = record.extrapolate(recordStorage3, propertime)
                        irec4 = record.extrapolate(recordStorage4, propertime)

                    #if (shouldInterpolate == True):
                        #irec1, irec2, irec3, irec4 = record.interpolate(prec1, prec2, prec3, prec4, rec1, rec2, rec3, rec4)
                    #else:
                        #shouldInterpolate = supposedToInterpolate
                    #prec1, prec2, prec3, prec4 = rec1, rec2, rec3, rec4
                    # OR
                    # prec1, prec2, prec3, prec4 = irec1, irec2, irec3, irec4

                    #filePathOriginal = '\\Users\\advai\\OneDrive\\Documents\\Visual Studio 2015\\Projects\\DolphinRacersLastStand\\Release\\DolphinRacersLastStand.exe'
                    #filePath2 = 'C:\\Users\\advai\\Google Drive\\2015-16 IMSA\\Summer SIR\\DolphinRacersLastStand\\Release'
                    subprocess.call([
                        '\\Users\\advai\\OneDrive\\Documents\\Visual Studio 2015\\Projects\\DolphinRacersLastStand\\Release\\DolphinRacersLastStand.exe',
                        str(irec1.latitude), str(irec1.longitude), str(irec2.latitude), str(irec2.longitude),
                        str(irec3.latitude), str(irec3.longitude), str(irec4.latitude), str(irec4.longitude),
                        heading_file, str(irec1.time)
                    ])
                    print("pass")
                    ifFirst = False
