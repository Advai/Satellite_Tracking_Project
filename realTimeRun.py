from time import time
import subprocess
import gps as gp
from time import time

"""This just makes two objects
one corresponds to GPS 1 and GPS 3
other goes to GPS 2 and GPS 4"""
gps13 = gp.GPS("COM3", 115200)
gps24 = gp.GPS("COM4", 115200)
time = str(time())
#The 4 withs open the textfile that stores each coordinate
with open("GPS1_" + time+".txt", "w") as f1:
    with open("GPS2_"+time+".txt", "w") as f2:
        with open("GPS3_"+time+".txt", "w") as f3:
            with open("GPS4_"+time+".txt", "w") as f4:
                while True:
                    #refer to method in gps.py class for explanation
                    arr1 = gps13.gps1234latlon(f1, f3, "GPS1", "GPS3")
                    arr2 = gps24.gps1234latlon(f2, f4, "GPS2", "GPS4")
                    #this checks to make sure that all 4 coordinates are passsed to the array and no time skips happened
                    if arr1 is None or arr2 is None:
                        print("fail")
                        print(arr1, arr2)
                        continue
                    else:
                        #calls the C++ program
                        subprocess.call(['\\Users\\advai\\OneDrive\\Documents\\Visual Studio 2015\\Projects\\DolphinRacersLastStand\\Release\\DolphinRacersLastStand.exe', str(arr1[0]), str(arr1[1]), str(arr2[0]), str(arr2[1]), str(arr1[2]), str(arr1[3]), str(arr2[2]), str(arr2[3]), 'headingRT_' +time+'.txt', str(arr1[5])])
                        print("pass")
