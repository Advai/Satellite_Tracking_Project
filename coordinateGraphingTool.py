import matplotlib.pyplot as plt
file = open("organizedStationaryRT2.txt", "r")
x = []
y = []
#plt.axis([41.78765, 41.78769, -88.3560, -88.35600009])
plt.xlim(41.78765, 41.78769)
plt.ylim(-88.3560, -88.35600009)
for line in file:
    arr = line.split(' ')
    x = [arr[1], arr[3], arr[5], arr[7]]
    y = [arr[0], arr[2], arr[4], arr[6]]
    plt.scatter(x, y)
plt.show()

