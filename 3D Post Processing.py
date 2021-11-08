#python verison 3.8.8
import serial
import math
import numpy as np
import open3d as o3d
#this is used to open teh port and set the port and the baud rate
s = serial.Serial("COM4", 115200)
print("Opening: " + s.name)
#open a file of xyz type
filename = "tof_radar.xyz"
coordinates = []
#this sends  1 bit to know when to start recording
s.write(b'1')
#open the file for reading
xyz = open(filename,"w")
counter=0
xcord=0
angle=0
samples=0
while(True):
    #decode the data into a string
    x = s.readline().decode()
    #x.strip('/r/n')
    result = [x.strip() for x in x.split(',')]
    counter = counter+1
    print(result) 
    if counter>6:
        samples=samples+1
        #obtain the distance mearuement from the array
        distance = float(result[1])
        #perfrom the distance calculations using trigonometric functions
        modangle = math.radians(angle)
        zcord = distance*math.sin(modangle)
        ycord = distance*math.cos(modangle)
        
        #write the coordinates to the file 
        xyz.write(str(xcord)+" "+str(ycord)+" "+str(zcord)+"\n")
        #increment angle each time to ensure we get 256 readings every 360 degrees
        angle +=1.40625
          
    #if the angle is bigger than 360 we reset and repeat for the next reading
    if angle>360:
        counter=0
        angle =0
        xcord+=200
    #once we reach 10 readings stop and exit the loop
    if(samples==2560):
        break;


#close the file and stop the reading
xyz.close()
s.close()

#create a point cloud variable using the open3D library
pcd = o3d.io.read_point_cloud("tof_radar.xyz", format='xyz')
#count the number of points in the cloud
numpoints = len(pcd.points)

lines = []
#join the points around every 360 circle with a line
i = 0
while (i < (numpoints/256)):
    lines.append([0+(256*i),255+(256*i)])
    for x in range(255):
        lines.append([x+(i*256),x+1+(i*256)])
    i += 1

i = 1
#use the lineset function to join the points in the cloud
line_set = o3d.geometry.LineSet(points=o3d.utility.Vector3dVector(np.asarray(pcd.points)), lines=o3d.utility.Vector2iVector(lines))
#do the final visualization using open3D using the draw_geometries function.
o3d.visualization.draw_geometries([line_set])

        
