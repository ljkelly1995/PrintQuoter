import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D

#Initialize variables
oldpos = [0,0]
currentpos = oldpos
totaltime = 0
startcheck = 0
newXY_vel = 1000
XY_acc = 4000 #mm/s^2
count = 0
xpoints = []
ypoints = []
zpoints = []
#setup Plot
fig = plt.figure()
ax = plt.axes(projection='3d')
#set Starting Z
currentZ = 0

#Start Gcode Scrape
f = open('topcap.txt', 'r')
doc = f.readlines()
enddoc = len(doc)
for line in doc:
    #exit loop
    count += 1
    if count >= enddoc:
        ax.scatter(xpoints, ypoints, zpoints, c='r', marker='o')
        plt.show()
        break
    if len(line) == 28:
        startcheck = 1
    if line[0:6] == "M204 S":
            XY_acc = float(line[6:10])    
    if line[0:2] == "G1" and startcheck == 1:
        #Update Z
        if len(line) > 3:
            if line[3] == "Z":
                currentZ = line[4:8]
        #Get Speed
        if line.find(" F") != -1:
            newXY_vel = float(line[line.find(" F")+2:line.find(" F")+6])
            #Check for z movement
        if len(line) > 3:
            if line[3] == "X":
                oldpos = currentpos
                #record X,Y
                if len(line) > 29:
                    if line[19] == "F":
                        currentpos = [float(line[4:11]), float(line[12:19])]
                    elif line[20] == "F":
                        if line[12] == "Y":
                            currentpos = [float(line[4:11]), float(line[13:19])]
                        elif line[11] == "Y":
                            currentpos = [float(line[4:11]), float(line[12:19])]
                        else:
                            currentpos = [float(line[4:11]), float(line[11:19])]
                    else:
                        if line[11] == "Y":
                            currentpos = [float(line[4:9]), float(line[12:18])]
                        else:
                            #print(line)
                            currentpos = [float(line[4:9]), float(line[13:19])] 
                elif len(line) == 29:
                    if line[12] == "Y":
                        currentpos = [float(line[4:11]), float(line[13:19])]                                                             
                    elif line[11] == "Y":
                        currentpos = [float(line[4:11]), float(line[12:19])]
                    else:
                        print("ERROR: Unrecognized gcode \nExcluding:", '"'+str(line[:-1])+'"'+"\nContinuing...")
                elif len(line) == 19:
                    currentpos = [float(line[4:11]), float(line[12:19])]
                elif len(line) == 20:
                    if line[12] == "Y":
                        currentpos = [float(line[4:9]), float(line[13:19])]
                    else:
                        currentpos = [float(line[4:9]), float(line[12:19])]
                elif len(line) == 21:
                    currentpos = [float(line[4:11]), float(line[13:21])]
                elif len(line) == 28:
                    currentpos = [float(line[4:11]), float(line[12:19])] 
                elif len(line) != 25:
                    currentpos = [float(line[4:10]), float(line[12:18])]  
                else:
                    print("ERROR: Unrecognized gcode \nExcluding:", '"'+str(line[:-1])+'"'+"\nContinuing...")
                #Update Point List
        if (count % 40) ==0:
            xpoints.append(int(currentpos[0]))
            ypoints.append(int(currentpos[1]))
            zpoints.append(float(currentZ))
            #Do Math
        cvt_XY_vel = newXY_vel/60
        MoveDistance = math.sqrt(math.pow((currentpos[0] - oldpos[0]),2) + math.pow((currentpos[1] - oldpos[1]),2))
        TimeToAcc = (cvt_XY_vel/XY_acc)
        DistToAcc = (cvt_XY_vel*TimeToAcc)/2
        if MoveDistance <= DistToAcc:
            #time = math.sqrt((2*MoveDistance)/XY_acc)
            #time = math.sqrt(2*MoveDistance/XY_acc)
            time = MoveDistance/cvt_XY_vel
        elif MoveDistance < 1000:
            #time = (TimeToAcc + (MoveDistance - DistToAcc)/(newXY_vel/60))
            time = (MoveDistance)/cvt_XY_vel
        else:
            print("REMOVED")
        totaltime += time

ttime_min = totaltime/60
hours = ttime_min/60
roundhour = math.floor(hours)
print("Total is: ",  roundhour, " Hours and ", math.floor((hours-roundhour)*60), " Minutes")
