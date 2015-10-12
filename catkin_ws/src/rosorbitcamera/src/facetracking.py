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
import rospy
import roslib
from time import sleep
from math import sqrt

UVCDYNCTRLEXEC="/usr/bin/uvcdynctrl"

# Set cascade classifier to use and camera ID (determined with "sudo uvcdynctrl -l")
faceCascade = cv.CascadeClassifier("/home/andreea/Documents/catkin_ws/src/rosorbitcamera/src/haarcascade_frontalface_default.xml")
deviceID = 1

def webcam_feed():
	print "Opening camera..."
	cap = cv.VideoCapture(deviceID)
	prevBestFace = (None, None)
	
	while(True):
		# Capture frame-by-frame
		ret, frame = cap.read()

		# Draw reference rectangle in the centre of the image
		cv.rectangle(frame, (270, 190), (370, 290), (0, 0, 255), 2)

		# Run detection
		faces = faceCascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=6, minSize=(50, 50), maxSize=(250, 250), flags=cv.cv.CV_HAAR_SCALE_IMAGE)
		
		if faces != () and faces.size > 0:		# OpenCv strangely returns empty tuples occasionally, so check for that
			bestFace = max(faces, key=lambda item:item[2])
			cv.rectangle(frame, (bestFace[0], bestFace[1]), (bestFace[0]+bestFace[2], bestFace[1]+bestFace[3]), (0, 255, 0), 2)

			bestFaceCentreX = bestFace[0]+bestFace[2]/2
			bestFaceCentreY = bestFace[1]+bestFace[2]/2

			# If the best face is too far away from one previously detected, it is probably a mis-detection, so ignore
			if prevBestFace != (None, None) and sqrt((bestFaceCentreX-prevBestFace[0])**2 + (bestFaceCentreY-prevBestFace[1])**2) > 250:
				continue

			imageCentreX = frame.shape[1]/2
			imageCentreY = frame.shape[0]/2
			correctionX = imageCentreX - bestFaceCentreX
			correctionY = imageCentreY - bestFaceCentreY

			if abs(correctionX)>80:
				#print "Pan ", "right: " if correctionX < 0 else "left: ", correctionX
				adjust_camera(correctionX, "Pan")
			if abs(correctionY)>80:
				#print "Tilt ", "up: " if correctionY < 0 else "down: ", correctionY
				adjust_camera(-correctionY, "Tilt")		# Camera interprets negative values as up and positive values as down, contrary to expectations

			prevBestFace = (bestFaceCentreX, bestFaceCentreY)

		if ret:
			cv.imshow( 'Camera' , frame )

		key = cv.waitKey(1)
		if key != -1:
			if key == ord('q'):
				break
			elif key == ord('r'):
				reset()


	cap.release()
	cv.destroyAllWindows()


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
	webcam_feed()

if __name__ == '__main__':
	main()
