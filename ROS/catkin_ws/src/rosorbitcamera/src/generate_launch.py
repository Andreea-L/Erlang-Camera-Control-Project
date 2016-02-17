import sys


f = open("face.launch", "w")

no_of_workers = sys.argv[1]
f.write("<launch>\n")
f.write("<node name=\"orbit_face_tracking_main\" pkg=\"rosorbitcamera\" type=\"facetracking.py\" args=\""+no_of_workers+"\" respawn=\"true\" output=\"screen\"/>\n")

classif = 1
for i in range(int(no_of_workers)):
	f.write("<node name=\"orbit_face_tracking_n"+str(i)+"\" pkg=\"rosorbitcamera\" type=\"worker.py\" args=\""+str(i)+" "+str(classif)+"\" respawn=\"true\" output=\"screen\"/>\n")
	classif+=1
	if classif==5:
		classif=1
f.write("</launch>")