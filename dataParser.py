import subprocess
import time
def nextLine(file):
    #this reads one line from the file
    arr = file.readline().split(' ')
    return arr
def splitFileArr(arr):
    for i in range(0, len(arr)):
        arr[i] = arr[i].split(" ")
    return arr
def findGreater(one, two):
    if(one<two):
        return one
    else:return two
def findMinLines(file, file2):
    fileLength = len(file.readlines())
    file2Length = len(file2.readlines())
    if(fileLength > file2Length):
        return file2Length
    else:
        return fileLength

"""This method will take two files and combine them into an intermediate file which is filled with the matched times and the corresponding
coordinates"""
def gps2FileTimeSort(file1str, file2str, intermediateFilestr):
    with open(file1str, "r") as file1:
        with open(file2str, "r") as file2:
            with open(intermediateFilestr, "w") as intermediateFile:
                #reads a new line from file 1 and file 2.
                gps1 = nextLine(file1)
                gps2 = nextLine(file2)
                counter = 0
                while not file1.closed and not file2.closed:
                    counter += 1
                    #This is a check that makes sure there are always coordinates passed to gps1 and gps2
                    if (len(gps1) < 3 or len(gps2) < 3):
                        break
                    time1 = gps1[2]
                    time2 = gps2[2]
                    if time1 != time2:
                        if time1 > time2:
                            gps2 = nextLine(file2)
                            continue
                        else:
                            gps1 = nextLine(file1)
                    else:
                        intermediateFile.write("%s %s %s %s %s" % (gps1[0],gps1[1], gps1[0], gps1[1], gps2[2]))
                        gps1 = nextLine(file1)
                        gps2 = nextLine(file2)
"""This will take the two intermediate files and combine them again by making sure the times
synch up and adds all 4 sets of coordinates into one file"""
def finalTimeSort(file5str, file6str, finalstr):
    with open(file5str, "r") as file5:
        with open(file6str, "r") as file6:
            with open(finalstr, "w") as final:
                gps1 = nextLine(file5)
                gps2 = nextLine(file6)
                counter = 0
                while not file5.closed and not file6.closed:
                    counter += 1
                    # print(counter)
                    if (len(gps1) < 3 or len(gps2) < 3):
                        break
                    time1 = gps1[4]
                    time2 = gps2[4]
                    if time1 != time2:
                        if time1 > time2:
                            gps2 = nextLine(file6)
                            continue
                        else:
                            gps1 = nextLine(file5)
                    else:
                        # print(counter)
                        #final.write("%s %s %s %s %s %s %s %s %s" % (gps1[0], gps1[1], gps2[0], gps2[1], gps1[2], gps1[3], gps2[2], gps2[3], gps2[4]))
                        gps1 = nextLine(file5)
                        gps2 = nextLine(file6)

gps2FileTimeSort("GPS1_1481744414.9156735.txt", "GPS2_1481744414.9156735.txt", "gps1-2finalStandBusTest.2.txt")
gps2FileTimeSort("GPS3_1481744414.9156735.txt", "GPS4_1481744414.9156735.txt", "gps3-4finalStandBusTest.2.txt")
finalTimeSort("gps1-2finalStandBusTest.2.txt", "gps3-4finalStandBusTest.2.txt", "organizedFinalStandBusTest.2.txt")

"""this next section will get the values from the final organized time file and pass them to the C++ Heading Program"""
count = 0
with open("organizedFinalStandBusTest.2.txt", "r") as f7:
    try:
        while True:
            gps = nextLine(f7)
            count += 1
            subprocess.call(['\\Users\\advai\\OneDrive\\Documents\\Visual Studio 2015\\Projects\\DolphinRacersLastStand\\Release\\DolphinRacersLastStand.exe', gps[0], gps[1], gps[2], gps[3], gps[4], gps[5], gps[6], gps[7], 'finalStandBusPostTestHeading.2.txt', gps[8]])
    #subprocess.call(['C:\\Users\\advai\\OneDrive\\Documents\\Visual Studio 2015\\Projects\\ConsoleApplication1\\Release\\ConsoleApplication1.exe', "1.7600666", "-88.32345", "41.76543", "-88.32492", "41.760034", "-88.32450", "41.76363", "-88.322323", "call-method.test.txt"])
    except IndexError:
        print(count)
        print("HIT A WALL")
