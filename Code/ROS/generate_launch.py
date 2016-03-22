import sys

## This script generates a .launch file, allowing ROS to manage node spwawning and lifetime.
##
## Author: Andreea Lutac


f = open("face.launch", "w")

no_of_workers = sys.argv[1]
rt = "_no_rt" if sys.argv[2]=="0" else ""
resp = "false" if sys.argv[3]=="0" else "true"
f.write("<launch>\n")
f.write("<node name=\"orbit_face_tracking_main\" pkg=\"rosorbitcamera\" type=\"facetracking"+rt+".py\" args=\""+no_of_workers+"\" respawn=\"false\" output=\"screen\"/>\n")

classif = 1
for i in range(int(no_of_workers)):
	f.write("<node name=\"orbit_face_tracking_n"+str(i)+"\" pkg=\"rosorbitcamera\" type=\"worker.py\" args=\""+str(i)+" "+str(classif)+"\" respawn=\""+resp+"\" output=\"screen\"/>\n")
	classif+=1
	if classif==5:
		classif=1
f.write("</launch>")