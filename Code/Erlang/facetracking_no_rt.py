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

import numpy as np
from random import randint
import time
import glob
import re

from erlport.erlterms import Atom, List
from erlport import erlang



def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)
    

def detect_face(frame, fid, worker):
	face_cascade = cv.CascadeClassifier("/home/andreea/Documents/catkin_ws/src/rosorbitcamera/src/HaarClassifiers/haarcascade_frontalface_1.xml")

	image = np.array(frame, dtype="uint8")
	best_face = []

	faces = face_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=6, minSize=(50, 50), flags=cv.cv.CV_HAAR_SCALE_IMAGE)
	if faces != () and faces.size > 0:		# OpenCv strangely returns empty tuples occasionally, so check for that
		best_face = max(faces, key=lambda item:item[2])
	if best_face!=[]:
		best_face = best_face.tolist()

	erlang.call(Atom("gen_server"), Atom("cast"), [(Atom("global"),Atom("aggregator_server")), (Atom("face"),fid, worker, best_face)])



def read_folder_feed(detectorsN, deviceID):
	pics={}
	j = 0
	for filename in natural_sort(glob.glob('/home/andreea/Pictures/Webcam/Input/*.jpg')):
		pics[j]=cv.imread(filename)
		j+=1
	j=0
	for key in pics.keys():
		frame = cv.cvtColor(pics[key], cv.COLOR_BGR2GRAY)

		message = (Atom("frame"),j+1,frame)
		time.sleep(0.3)
		
		receiver = randint(1,detectorsN)
		erlang.call(Atom("gen_server"), Atom("cast"), [(Atom("global"),receiver), message])
