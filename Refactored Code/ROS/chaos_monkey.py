## This script randomly terminates a number of ROS nodes,
## either "gracefully" or brutally.
##
## Author: Andreea Lutac

from subprocess import call
import sys
import random

kill_n = sys.argv[1]
worker_n = sys.argv[2]
kill_type = sys.argv[3]

for x in random.sample(range(0, int(worker_n)), int(kill_n)):
	if kill_type == "stop":
		call(["rosnode", "kill","/orbit_face_tracking_n"+str(x)])
	elif kill_type == "kill":
		call(["pkill", "-f", "orbit_face_tracking_n"+str(x),"-9"])
	elif kill_type == "main":
		call(["pkill", "-f", "orbit_face_tracking_main","-9"])

print "Finished killing."