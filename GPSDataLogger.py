import gps as gp
#we started from the end of teh road to a lamp post

fileName = "DGPSTest7.csv"
ifReal = True
data = []
COM = "COM8"
baud = 115200
gps = gp.GPS(data, ifReal, COM, baud)


print("The file you are writing to is: " + fileName)
input("Press the quit button if this is not correct")

count = 0

with open(fileName, 'w') as f1:
    while True:
        try:
            if(gps.is_fixed()):
                gps.refresh()
                f1.write("%s,%s,%s\n" % (gps.get_lat(), gps.get_lon(), gps.get_time()))
                print("recording..." + str(count))
                count+=1
        except KeyboardInterrupt:
            print("quit by keyboard")
            break