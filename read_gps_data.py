file_ = open("ard_output.txt", "r")
for line in file_:
    myList = line.split(' ')
    lat = myList[0]
    lon = myList[1]
    mylist = myList[0].split(",")
    mylist = myList[0].split(",")
    mylist1 = myList[1].split("\n")
    print(mylist1[0])
file_.close()