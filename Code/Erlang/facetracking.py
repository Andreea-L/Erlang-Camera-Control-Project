#!/usr/bin/env python

## This script encompasses the Python functions accessed by the interpreter instances
## created by each Erlang process.
##
## Author: Andreea Lutac


import cv2 as cv

import subprocess
import numpy as np
from random import randint
import time

from erlport.erlterms import Atom, List
from erlport import erlang



UVCDYNCTRLEXEC="/usr/bin/uvcdynctrl"
frame_h = 640
frame_w = 480

# Detects a face within a frame using an OpenCV cascade classifier;
# called by the Erlang face_servers
def detect_face(frame, fid, worker):
	face_cascade = cv.CascadeClassifier("/home/andreea/Documents/catkin_ws/src/rosorbitcamera/src/HaarClassifiers/haarcascade_frontalface_1.xml")
	image = np.array(frame, dtype="uint8")

	best_face = []

	faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=6, minSize=(50, 50), flags=cv.cv.CV_HAAR_SCALE_IMAGE)
	if faces != () and faces.size > 0:		# OpenCv strangely returns empty tuples occasionally, so check for that
		best_face = max(faces, key=lambda item:item[2])

	if best_face!=[]:
		best_face = best_face.tolist()

	# Send the resulting face as a message to the aggregator
	erlang.call(Atom("gen_server"), Atom("cast"), [(Atom("global"),Atom("aggregator_server")), (Atom("face"),fid, worker, best_face)])


# Opens a feed to the camera device and acquires images frame by frame;
# called by the Erlang interface
def read_webcam_feed(detectorsN, deviceID):
	cap = cv.VideoCapture(deviceID)

	while True:
		ret, frame = cap.read()		
		message = (Atom("frame"),j,frame) if ret else Atom("error")
		
		# Send the frame to a random Erlang detector process
		receiver = randint(1,detectorsN)
		erlang.call(Atom("gen_server"), Atom("cast"), [(Atom("global"),receiver), message])

# Calculates adjustments needed to re-centre the camera's gaze on the face and
# sends the commands to the device;
# called by the Erlang aggregator_server
def track_face(best_face):
	global frame_h, frame_w

	best_face_centre_x = best_face[0]+best_face[2]/2
	best_face_centre_y = best_face[1]+best_face[2]/2

	image_centre_x = frame_h/2
	image_centre_y = frame_w/2
	correction_x = image_centre_x - best_face_centre_x
	correction_y = image_centre_y - best_face_centre_y

	if abs(correction_x)>control_threshold:
		adjust_camera(correction_x, "Pan")
	if abs(correction_y)>control_threshold:
		adjust_camera(-correction_y, "Tilt")		# Camera interprets negative values as up and positive values as down, contrary to expectations



# Controls pan/tilt of camera
def adjust_camera(value, control):
	subprocess.Popen([UVCDYNCTRLEXEC, "-d", "video"+str(deviceID), "-s", control+" (relative)", "--", str(value)])

