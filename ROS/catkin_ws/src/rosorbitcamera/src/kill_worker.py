from subprocess import call
import sys
import random

killn = sys.argv[1]
workern = sys.argv[2]
killtype = sys.argv[3]

for x in random.sample(range(0, int(workern)), int(killn)):
	if killtype == "stop":
		call(["rosnode", "kill","/orbit_face_tracking_n"+str(x)]
	elif killtype == "kill":
		call(["pkill", "-f", "orbit_face_tracking_n"+str(x),"-9"])
	elif killtype == "main":
		call(["pkill", "-f", "orbit_face_tracking_main","-9"])

print "Finished killing."