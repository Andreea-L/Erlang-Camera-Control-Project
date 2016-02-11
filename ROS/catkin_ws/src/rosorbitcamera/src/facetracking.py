#!/usr/bin/env python

## This script is meant to enable face tracking on a Logitech Orbit MP camera,
## using OpenCV's Haar Cascade Classifier functions.
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
from math import sqrt
from collections import deque
from sensor_msgs.msg import Image
from rosorbitcamera.msg import Int32Numpy

UVCDYNCTRLEXEC="/usr/bin/uvcdynctrl"

# Set cascade classifier to use and camera ID (determined with "sudo uvcdynctrl -l")
deviceID = 1

historical_faces = deque(maxlen=100)
a_j = 0

a_f = open("/home/andreea/Documents/catkin_ws/src/rosorbitcamera/src/aggregator_timing.time", "a") 
pub_f = open("/home/andreea/Documents/catkin_ws/src/rosorbitcamera/src/publishing_timing.time", "a")
f = open("/home/andreea/Documents/catkin_ws/src/rosorbitcamera/src/roundtrip_timing.time", "a")

def webcam_feed(pub):
	global frame,f

	T = int(time() * 1000)
	print "Main node started at: ", T
	# f = open("/home/andreea/Documents/catkin_ws/src/rosorbitcamera/src/main_timing.time", "a")
	# f.write(str(T)+"\n\n")
	# f.close()

	print "Opening camera..."
	cap = cv.VideoCapture(deviceID)
	rate = rospy.Rate(3)

	
	j = 0
	while not rospy.is_shutdown():
		# Capture frame-by-frame
		ret, frame = cap.read()
		msg = bridge.cv2_to_imgmsg(frame)

		f.write("s:"+str(j)+":"+str(int(time() * 1000))+"\n")
		j+=1
		start_pub = int(time() * 1000)
		pub.publish(msg)
		end_pub = int(time() * 1000)
		rate.sleep()
		pub_f.write(str(end_pub-start_pub)+"\n")
		#print "Published frame ", j


		workers = pub.get_num_connections()
		subscribers = []
		for i in xrange(workers):
			subscribers += [rospy.Subscriber('orbit_faces'+str(i), Int32Numpy, display_face, callback_args=[i, pub, cap])]
	f.close()

def display_face(faceCoord, args):
	global frame, historical_faces, a_j,a_f

	a_f.write("a:"+str(a_j)+":"+str(int(time() * 1000))+"\n")
	a_j+=1

	faceCoord = faceCoord.data
	workerID = args[0]
	pub = args[1]
	cap = args[2]

	if len(faceCoord) == 4:
		historical_faces.append(faceCoord)

	bestFace = map(lambda y: sum(y) / len(y), zip(*historical_faces))

	#print bestFace
	cv.rectangle(frame, (270, 190), (370, 290), (0, 0, 255), 2)
	if bestFace:
		cv.rectangle(frame, (bestFace[0], bestFace[1]), (bestFace[0]+bestFace[2], bestFace[1]+bestFace[3]), (0, 255, 0), 2)


	# bestFaceCentreX = bestFace[0]+bestFace[2]/2
	# bestFaceCentreY = bestFace[1]+bestFace[2]/2

	# imageCentreX = frame.shape[1]/2
	# imageCentreY = frame.shape[0]/2
	# correctionX = imageCentreX - bestFaceCentreX
	# correctionY = imageCentreY - bestFaceCentreY


	# if abs(correctionX)>80:
	# 	#print "Pan ", "right: " if correctionX < 0 else "left: ", correctionX
	# 	adjust_camera(correctionX, "Pan")
	# if abs(correctionY)>80:
	# 	#print "Tilt ", "up: " if correctionY < 0 else "down: ", correctionY
	# 	adjust_camera(-correctionY, "Tilt")		# Camera interprets negative values as up and positive values as down, contrary to expectations

	cv.imshow( 'Result' , frame )

	key = cv.waitKey(1)
	if key != -1 and key == ord('q'):
		cap.release()
		cv.destroyAllWindows()
		sys.exit()


# Controls pan/tilt of camera
def adjust_camera(value, control):
	subprocess.Popen([UVCDYNCTRLEXEC, "-d", "video"+str(deviceID), "-s", control+" (relative)", "--", str(value)])


# Pan/Tilt Reset	
def reset():
	subprocess.Popen([UVCDYNCTRLEXEC, "-d", "video"+str(deviceID), "-s", "Pan Reset", "3"])
	sleep(3)
	subprocess.Popen([UVCDYNCTRLEXEC, "-d", "video"+str(deviceID), "-s", "Tilt Reset", "3"])
	sleep(3)


def main():

	rospy.init_node('orbit_face_tracking_main', anonymous=True)
	pub = rospy.Publisher('orbit_images', Image, queue_size=10)
	webcam_feed(pub)

if __name__ == '__main__':
	main()