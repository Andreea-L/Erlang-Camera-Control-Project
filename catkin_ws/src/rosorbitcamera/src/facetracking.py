#!/usr/bin/env python
import cv2 as cv
cv.namedWindow('Camera', cv.WINDOW_AUTOSIZE)

import cv_bridge as cvROS
import gtk
import subprocess
import rospy
import roslib
import time

UVCDYNCTRLEXEC="/usr/bin/uvcdynctrl"

## The value indicates amount of movement for panning and tilt
## Max Ranges (determined with uvcdynctrl -v -c):
## 	Tilt = -1920 to 1920
##	Pan  = -4480 to 4480
faceCascade = cv.CascadeClassifier("/home/andreea/Documents/catkin_ws/src/rosorbitcamera/src/haarcascade_frontalface_default.xml")
deviceID = 1

def webcam_feed():
	print "Opening camera..."
	cap = cv.VideoCapture(deviceID)
	
	while(True):
		# Capture frame-by-frame
		ret, frame = cap.read()
		cv.rectangle(frame, (270, 190), (370, 290), (0, 0, 255), 2)
		faces = faceCascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=6, minSize=(30, 30), flags=cv.cv.CV_HAAR_SCALE_IMAGE)
		if faces != () and faces.size > 0:
			bestFace = max(faces, key=lambda item:item[2])
			cv.rectangle(frame, (bestFace[0], bestFace[1]), (bestFace[0]+bestFace[2], bestFace[1]+bestFace[3]), (0, 255, 0), 2)

			#print "X: ", bestFace[0], "Y: ", bestFace[1],"W: ", bestFace[0]+bestFace[2], "H: ", bestFace[1]+bestFace[3]
			imageCentreX = frame.shape[1]/2
			imageCentreY = frame.shape[0]/2

			#print imageCentreX
			bestFaceCentreX = bestFace[0]+bestFace[2]/2
			bestFaceCentreY = bestFace[1]+bestFace[2]/2
			correctionX = imageCentreX - bestFaceCentreX
			correctionY = imageCentreY - bestFaceCentreY

			if abs(correctionX)>80:
				print "Pan ", "right: " if correctionX < 0 else "left: ", correctionX
				pan(correctionX)
			if abs(correctionY)>80:
				print "Tilt ", "up: " if correctionY < 0 else "down: ", correctionY
				tilt(-correctionY)

		if ret:
			cv.imshow( 'Camera' , frame )

		key = cv.waitKey(1)
		if key != -1:
			if key == ord('q'):
				break
			elif key == ord('r'):
				ptReset()


	cap.release()
	cv.destroyAllWindows()

def tilt(value):
	control = "Tilt (relative)"
	subprocess.Popen([UVCDYNCTRLEXEC, "-d", "video"+str(deviceID), "-s", control, "--", str(value)])
	return True

def pan(value):
	control = "Pan (relative)"
	subprocess.Popen([UVCDYNCTRLEXEC, "-d", "video"+str(deviceID), "-s", control, "--", str(value)])
	return True


# Pan/Tilt Reset	
def ptReset():
	subprocess.Popen([UVCDYNCTRLEXEC, "-d", "video"+str(deviceID), "-s", "Pan Reset", "3"])
	time.sleep(3)
	subprocess.Popen([UVCDYNCTRLEXEC, "-d", "video"+str(deviceID), "-s", "Tilt Reset", "3"])
	time.sleep(3)
	return True

webcam_feed()


