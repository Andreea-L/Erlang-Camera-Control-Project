#!/usr/bin/env python

## This script runs the main image acquisition node for the ROS facetracking system,
## in addition to being responsible for aggregating the faces and controlling the camera.
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


import subprocess
import sys
import rospy
import roslib
from time import sleep, time
from random import randint
from math import sqrt
from collections import deque
from sensor_msgs.msg import Image
from rosorbitcamera.msg import Int32Numpy

# Path to library that enables camera control
UVCDYNCTRLEXEC="/usr/bin/uvcdynctrl"

# Set camera ID (determined with "sudo uvcdynctrl -l")
device_ID = 1
control_threshold=80 	# Set when an adjustment to the position should be made
historical_faces = deque(maxlen=1)

# Opens a feed to the camera device and acquires images frame by frame,
# publishing them to a randomly-chosen "camera_frames" topic
def webcam_feed(publishers):
	global frame

	print "Opening camera..."

	cap = cv.VideoCapture(device_ID)
	
	rate = rospy.Rate(10)
	
	j = 0
	while not rospy.is_shutdown():
		# Capture frame-by-frame
		ret, frame = cap.read()

		msg = bridge.cv2_to_imgmsg(frame)
		pub = publishers[randint(0,len(publishers)-1)]

		msg.header.frame_id = str(j)
		pub.publish(msg)
		rate.sleep()

# Aggregates the faces received from the detectors,
# displays the "best" face, calculates adjustments needed to re-centre 
# the camera's gaze on the face and sends the commands to the device
def aggregate_face(face_coord, args):
	global frame, historical_faces

	face_ID = face_coord.data[-1]


	face_coord = face_coord.data[:-1]
	worker_ID = args[0]
	cap = args[1]

	
	if len(face_coord) == 4:
		historical_faces.append(face_coord)

	best_face = map(lambda y: sum(y) / len(y), zip(*historical_faces))

	cv.rectangle(frame, (270, 190), (370, 290), (0, 0, 255), 2)
	if best_face:
		cv.rectangle(frame, (best_face[0], best_face[1]), (best_face[0]+best_face[2], best_face[1]+best_face[3]), (0, 255, 0), 2)


	best_face_centre_x = best_face[0]+best_face[2]/2
	best_face_centre_y = best_face[1]+best_face[2]/2

	image_centre_x = frame.shape[1]/2
	image_centre_y = frame.shape[0]/2
	correction_x = image_centre_x - best_face_centre_x
	correction_y = image_centre_y - best_face_centre_y

	if abs(correction_x)>control_threshold:
		adjust_camera(correction_x, "Pan")
	if abs(correction_y)>control_threshold:
		adjust_camera(-correction_y, "Tilt")		# Camera interprets negative values as up and positive values as down, contrary to expectations

	cv.imshow( 'Result' , frame )

	key = cv.waitKey(1)
	if key != -1 and key == ord('q'):
		cap.release()
		cv.destroyAllWindows()
		sys.exit()


# Controls pan/tilt of camera
def adjust_camera(value, control):
	subprocess.Popen([UVCDYNCTRLEXEC, "-d", "video"+str(device_ID), "-s", control+" (relative)", "--", str(value)])


# Pan/Tilt Reset	
def reset():
	subprocess.Popen([UVCDYNCTRLEXEC, "-d", "video"+str(device_ID), "-s", "Pan Reset", "3"])
	sleep(3)
	subprocess.Popen([UVCDYNCTRLEXEC, "-d", "video"+str(device_ID), "-s", "Tilt Reset", "3"])
	sleep(3)


def main():
	expected_workers = int(sys.argv[1])
	rospy.init_node('face_tracking_main')
	
	# Create frame topics
	publishers = []
	for i in xrange(expected_workers):
		publishers += [ rospy.Publisher('camera_frames_'+str(i), Image, queue_size=1000) ]

	# Subscribe to face topics
	subscribers = []
	for i in xrange(len(publishers)):
		subscribers += [rospy.Subscriber('camera_faces_'+str(i), Int32Numpy, display_face, callback_args=[i, cap])]
	webcam_feed(publishers)

if __name__ == '__main__':
	main()