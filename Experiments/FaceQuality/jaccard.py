import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches



def jaccard_index(tup, sys, i):

	actual_rec = [ int(x) for x in tup[0] ]
	guess_rec = [ int(x) for x in tup[1] ]
	fig1 = plt.figure()
	ax1 = fig1.add_subplot(111, aspect='equal')
	ax1.add_patch(
	    patches.Rectangle(
	        (actual_rec[0], actual_rec[1]),   # (x,y)
	        actual_rec[2]-actual_rec[0],          # width
	        actual_rec[3]-actual_rec[1],
	        hatch='/',
	        facecolor = "green"         # height
	    )
	)
	ax1.add_patch(
	    patches.Rectangle(
	        (guess_rec[0], guess_rec[1]),   # (x,y)
	        guess_rec[2]-guess_rec[0],          # width
	        guess_rec[3]-guess_rec[1],
	        hatch='\\'         # height
	    )
	)
	ax1.set_xlim(0,600)
	ax1.set_ylim(0,600)
	fig1.savefig("rect_"+sys+str(i)+".png", dpi=90, bbox_inches='tight')
	plt.close()

	overlap_start = (max(actual_rec[0],guess_rec[0]), max(actual_rec[1],guess_rec[1]))
	overlap_end = (min(actual_rec[2],guess_rec[2]), min(actual_rec[3],guess_rec[3]))

	if overlap_end[0]-overlap_start[0]<0 or overlap_end[1]-overlap_start[1]<0:
		return 0

	actual_area = (actual_rec[0]-actual_rec[2])**2
	detected_area = (guess_rec[0]-guess_rec[2])**2
	overlap_area = (overlap_end[0]-overlap_start[0])**2
	return overlap_area/(float(actual_area)+float(detected_area))


f = open("face.coord")
lines = f.readlines()

val = [ x.split(":") for x in lines	]

actual = [ x[1].split(" ") for x in val if x[0]=="ACTUAL"]
ros = [ x[1].split(" ") for x in val if x[0]=="ROS"]
erl = [ [x[1],x[2].split(" ")] for x in val if x[0]=="ERL"]
diff_1 = [jaccard_index(x[1], "ros", x[0]) for x in enumerate(zip(actual, ros))]
diff_2 = [jaccard_index([actual[int(x[1][0])], x[1][1]], "erl", x[0]) for x in enumerate(erl)]

print "Jaccard index of similarity, as detected by one ROS node: ",sum(diff_1)/float(len(diff_1))
print "Jaccard index of similarity, as detected by one ERL node: ",sum(diff_2)/float(len(diff_2))
