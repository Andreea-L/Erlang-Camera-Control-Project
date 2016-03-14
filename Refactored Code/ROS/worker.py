#!/usr/bin/env python

## This script runs the worker ROS nodes which perform face detection
## using OpenCV cascade classifiers for Haar-like features.
##
## Author: Andreea Lutac

import cv2 as cv
cv.namedWindow('Camera', cv.WINDOW_AUTOSIZE)

import cv_bridge as cvROS
bridge = cvROS.CvBridge()

import sys
import rospy
import roslib
import time
from sensor_msgs.msg import Image
from rosorbitcamera.msg import Int32Numpy

# Detects a face within a frame using an OpenCV cascade classifier;
def detect_face(msg, args):
	frame_ID = int(msg.header.frame_id)
	frame = bridge.imgmsg_to_cv2(msg)

	# Run detection
	face_cascade=args[2]
	faces = face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=6, minSize=(50, 50), flags=cv.cv.CV_HAAR_SCALE_IMAGE)

	best_face = []
	if faces != () and faces.size > 0:		# OpenCv strangely returns empty tuples occasionally, so check for that
		best_face = max(faces, key=lambda item:item[2])
	
	pub=args[0]
	rate=args[1]
	pub.publish(best_face.tolist()+[frame_ID] if best_face != [] else [frame_ID])
	rate.sleep()



def main():
	node_ID = sys.argv[1]
	suffix = sys.argv[2]

	# Set cascade classifier to use
	face_cascade = cv.CascadeClassifier("/home/andreea/Documents/catkin_ws/src/rosorbitcamera/src/HaarClassifiers/haarcascade_frontalface_1.xml")

	rospy.init_node('face_tracking_n'+str(node_ID), anonymous=True)

	# Subscripe to dedicated frame topic and create face topic
	pub = rospy.Publisher('camera_faces_'+str(node_ID), Int32Numpy, queue_size=10)
	rospy.Subscriber('camera_frames_'+str(node_ID), Image, detect_face, callback_args=[pub,rospy.Rate(10),face_cascade])
	rospy.spin()

if __name__ == '__main__':
	main()
