import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pprint


def jaccard_index(tup, sys, i):
	actual_rec = [ int(x) for x in tup[0] ]
	guess_rec = [ int(x) for x in tup[1] ]

	overlap_start = (max(actual_rec[0],guess_rec[0]), max(actual_rec[1],guess_rec[1]))
	overlap_end = (min(actual_rec[2],guess_rec[2]), min(actual_rec[3],guess_rec[3]))

	if overlap_end[0]-overlap_start[0]<0 or overlap_end[1]-overlap_start[1]<0:
		return 0

	actual_area = (actual_rec[0]-actual_rec[2])**2
	detected_area = (guess_rec[0]-guess_rec[2])**2
	overlap_area = (overlap_end[0]-overlap_start[0])**2
	return overlap_area/(float(actual_area)+float(detected_area))


val = [ x.split(":") for x in open("/home/andreea/Pictures/Webcam/Faces/face.coord").readlines() ]
actual = [ x[1].split(" ") for x in val if x[0]=="ACTUAL"]

names=["10", "25", "50","75","90"]
files_stop = [ open(f+"stop.coord") for f in names ]
files_kill = [ open(f+"kill.coord") for f in names ]
main_kill = open("mainkill.coord")
agg_kill = open("aggkill.coord")

res = open("jaccard.idx","a+")

i=0
for f in files_stop:
	res.write( "######100 nodes, "+str(names[i])+" nodes stopped.\n")
	values = [ x.split(":") for x in f.readlines() ]
	ros = [ [x[1],x[2].split(" ")] for x in values if x[0]=="ROS"]
	erl = [ [x[1],x[2].split(" ")] for x in values if x[0]=="ERL"]
	res.write("\n##Jaccard index of similarity variation (ROS):\n")
	for idx in [ jaccard_index([actual[int(x[0])], x[1]], "ros", x[0]) for x in ros[:-1]]: 
		res.write('%.3f ' % idx)
	res.write("\n##Jaccard index of similarity variation (ERL):\n")
	for idx in [ jaccard_index([actual[int(x[0])], x[1]], "erl", x[0]) for x in erl]:
		res.write('%.3f ' % idx)
	res.write("\n\n")
	i+=1


i=0
for f in files_kill:
	res.write( "######100 nodes, "+str(names[i])+" nodes killed.\n")
	values = [ x.split(":") for x in f.readlines() ]
	ros = [ [x[1],x[2].split(" ")] for x in values if x[0]=="ROS"]
	erl = [ [x[1],x[2].split(" ")] for x in values if x[0]=="ERL"]
	res.write("\n##Jaccard index of similarity variation (ROS):\n")
	for idx in [ jaccard_index([actual[int(x[0])], x[1]], "ros", x[0]) for x in ros[:-1]]:
		res.write('%.3f ' % idx)
	res.write("\n##Jaccard index of similarity variation (ERL):\n")
	for idx in [ jaccard_index([actual[int(x[0])], x[1]], "erl", x[0]) for x in erl]:
		res.write('%.3f ' % idx)
	res.write("\n\n")
	i+=1
