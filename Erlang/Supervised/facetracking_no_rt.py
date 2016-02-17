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
cv.namedWindow('Camera', cv.WINDOW_AUTOSIZE)

#import cv_bridge as cvROS
import subprocess
import numpy as np
from random import randint
import time
import zlib
import glob
import re

from erlport.erlterms import Atom, List
from erlport import erlang



UVCDYNCTRLEXEC="/usr/bin/uvcdynctrl"

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

def detect_face(frame, fid, worker):
	print "PY: Received frame."
	# f = open("/home/andreea/Documents/ErlangProject/Supervised/Timing/roundtrip_timing_py.time", "a") 
	# f.write("PYg:"+str(fid)+":"+str(int(time.time() * 1000000000))+"\n")

	suffix = randint(1,4)
	faceCascade = cv.CascadeClassifier("/home/andreea/Documents/catkin_ws/src/rosorbitcamera/src/HaarClassifiers/haarcascade_frontalface_"str(suffix)+".xml")

	#flat_frame = zlib.decompress(frame)
	#flat_frame = [int(i) for i in flat_frame.split(" ")]
	image = np.array(frame, dtype="uint8")
	#image = np.reshape(image, (480, 640))
	bestFace = []

	faces = faceCascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=6, minSize=(50, 50), maxSize=(300, 250), flags=cv.cv.CV_HAAR_SCALE_IMAGE)
	if faces != () and faces.size > 0:		# OpenCv strangely returns empty tuples occasionally, so check for that
		bestFace = max(faces, key=lambda item:item[2])
	#print "PY: Detection finished. Face found? ", True if bestFace!=[] else False
	if bestFace!=[]:
		bestFace = bestFace.tolist()


	# f.write("PYf:"+str(fid)+":"+str(int(time.time() * 1000000000))+"\n")
	# f.close()
	print bestFace
	erlang.call(Atom("gen_server"), Atom("cast"), [(Atom("global"),Atom("aggregator_server")), (Atom("face"),fid, worker, bestFace)])



def read_webcam_feed(detectorsN, deviceID):

	#cap = cv.VideoCapture(deviceID)
	#i=0
	pics={}
	j = 0
	for filename in natural_sort(glob.glob('/home/andreea/Pictures/Webcam/*.jpg')):
		pics[j]=cv.imread(filename)
		j+=1
	j=0
	for key in pics.keys():
		# #ret, frame = cap.read()
		# T = int(time.time() * 1000)
		# fps = open("/home/andreea/Documents/ErlangProject/Supervised/Timing/main_timing.time", "a+")
		# fps.write(str(T)+"\n\n")
		# fps.close()
		
		frame = cv.cvtColor(pics[key], cv.COLOR_BGR2GRAY)
		
		#c_frame = zlib.compress(' '.join(str(e) for f in frame for e in f),9)
		message = (Atom("frame"),j,frame)
		#i+=1
		print "PY: Sending frame..."
		time.sleep(0.5)
		
		receiver = randint(0,detectorsN)
		f = open("/home/andreea/Documents/ErlangProject/Supervised/Timing/roundtrip_timing_py.time", "a") 
		f.write("PYs:"+str(j)+":"+str(int(time.time() * 1000000000))+"\n")
		j+=1
		erlang.call(Atom("gen_server"), Atom("cast"), [(Atom("global"),receiver), message])

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


# Controls pan/tilt of camera
def adjust_camera(value, control):
	subprocess.Popen([UVCDYNCTRLEXEC, "-d", "video"+str(deviceID), "-s", control+" (relative)", "--", str(value)])


# Pan/Tilt Reset	
def reset():
	subprocess.Popen([UVCDYNCTRLEXEC, "-d", "video"+str(deviceID), "-s", "Pan Reset", "3"])
	sleep(3)
	subprocess.Popen([UVCDYNCTRLEXEC, "-d", "video"+str(deviceID), "-s", "Tilt Reset", "3"])
	sleep(3)
