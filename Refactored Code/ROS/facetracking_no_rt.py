#!/usr/bin/env python

## This script runs the main image acquisition node for the ROS facetracking system,
## in addition to being responsible for aggregating the faces.
## THIS SCRIPT IS NON-REAL-TIME
##
## Max pan/tilt angles of camera (determined with "uvcdynctrl -v -c"):
## 	Tilt = -1920 to 1920
##	Pan  = -4480 to 4480
##
## Author: Andreea Lutac


import cv2 as cv
cv.namedWindow('Result', cv.WINDOW_AUTOSIZE)
frame = None

import cv_bridge as cvROS
bridge = cvROS.CvBridge()

import sys
import rospy
import roslib
from time import sleep, time
from random import randint
from math import sqrt, ceil
from collections import deque
from sensor_msgs.msg import Image
from rosorbitcamera.msg import Int32Numpy

import glob
import re

historical_faces = deque(maxlen=3)

pics={}


def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)


def webcam_feed(publishers):
	global frame, pics

	T = int(time() * 1000)
	print "Main node started at: ", T

	rate = rospy.Rate(5)

	subscribers = []
	for i in xrange(len(publishers)):
		subscribers += [rospy.Subscriber('orbit_faces'+str(i), Int32Numpy, display_face, callback_args=[i])]
	j = 1
	for filename in natural_sort(glob.glob('/home/andreea/Pictures/Webcam/Input/*.jpg')):
		pics[j]=cv.imread(filename)
		j+=1
	
	
	while not rospy.is_shutdown():
		for key in pics.keys():
			msg = bridge.cv2_to_imgmsg(pics[key]) 

			pub = publishers[randint(0,len(publishers)-1)]
			
			msg.header.frame_id = str(key)

			pub.publish(msg)
			rate.sleep()

		rospy.signal_shutdown("finished")

	f.close()

def display_face(faceCoord, args):
	global frame, historical_faces, pics

	face_ID = face_coord.data[-1]


	face_coord = face_coord.data[:-1]
	worker_ID = args[0]
	cap = args[1]

	
	if len(face_coord) == 4:
		historical_faces.append(face_coord)

	best_face = map(lambda y: sum(y) / len(y), zip(*historical_faces))

	image = pics[face_ID]
	start_coord = (0,0)
	end_coord = (0,0)
	if best_face:
		start_coord = (best_face[0], best_face[1])
		end_coord = (best_face[0]+best_face[2], best_face[1]+best_face[3])
		cv.rectangle(image, (best_face[0], best_face[1]), (best_face[0]+best_face[2], best_face[1]+best_face[3]), (0, 255, 0), 2)

	
	
	res_file = open("/home/andreea/Pictures/Webcam/Faces/face.coord","a+")
	res_file.write("ROS:"+str(faceID)+":"+str(start_coord[0])+" "+str(start_coord[1])+" "+str(end_coord[0])+" "+str(end_coord[1])+"\n")
	res_file.close()


def main():
	expected_workers = int(sys.argv[1])
	rospy.init_node('orbit_face_tracking_main', anonymous=True)
	
	publishers = []
	for i in xrange(expected_workers):
		publishers += [ rospy.Publisher('orbit_images'+str(i), Image, queue_size=1000) ]
	webcam_feed(publishers)

if __name__ == '__main__':
	main()