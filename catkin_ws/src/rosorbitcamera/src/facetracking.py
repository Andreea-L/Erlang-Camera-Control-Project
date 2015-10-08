#!/usr/bin/env python
########################################################
# Created by: Steve Cundy
# Date Modified: Jan 29, 2008
#
# Purpose: quick and dirty gui to control PTZ of my
# Logitech Quickcam Orbit AF (actually there is no zoom
# control :)
#
# To Do:
# - Modify icons and labels
# - Detect difference between click and hold for
#	continued movement of cam
# - Find out what doesn't work
# - Actually learn how to code in python instead of
#	hacking together other peoples code
########################################################

import cv2 as cv
cv.namedWindow('Camera', cv.WINDOW_AUTOSIZE)
import cv_bridge as cvROS
import gtk
import subprocess
import rospy
import roslib
import time


## The following imports aren't needed??
#import pygtk
#import gobject
#from subprocess import *

## The full path to uvcdynctrl
UVCDYNCTRLEXEC="/usr/bin/uvcdynctrl"

## The value indicates amount of movement for panning and tilt
## Max Ranges (determined with uvcdynctrl -v -c):
## 	Tilt = -1920 to 1920
##	Pan  = -4480 to 4480
faceCascade = cv.CascadeClassifier("/home/andreea/Documents/catkin_ws/src/rosorbitcamera/src/haarcascade_frontalface_default.xml")
deviceName = "video1"
step = 250
panRight = tiltUp = str(-step)
panLeft = tiltDown = str(step)

## Declare the main class
class ccUVCPTZ_Main:
	## Define the init script to initialize the application
	def __init__(self):
		## Prep the Main Window for stuff
		rospy.init_node('orbit', anonymous = True)
		
		window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		window.set_title("ccUVCPTZ")
		window.connect("delete_event", self.hide, window)
		window.connect("window-state-event", self.window_event, window)

		## Create a StatusIcon for the app
		statusIcon = gtk.StatusIcon()

		## Let's build the menu for the StatusIcon
		self.sMenu = gtk.Menu()
		menuItem = gtk.ImageMenuItem(gtk.STOCK_OPEN)
		menuItem.connect('activate', self.activate_window, window)
		self.sMenu.append(menuItem)
		menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
		menuItem.connect('activate', self.exit, statusIcon)
		self.sMenu.append(menuItem)

		## Don't forget to include the icon actions itself
		statusIcon.set_from_stock(gtk.STOCK_HOME)
		statusIcon.set_tooltip("StatusIcon test")
		statusIcon.connect('activate', self.activate_window, window)
		statusIcon.connect('popup-menu', self.popup_menu, self.sMenu)
		statusIcon.set_visible(True)

		## Let's use a table to make a nice pretty grid for our buttons
		self.table = gtk.Table(5, 3, True)
		window.add(self.table)
		## Time to build the buttons
		# Tilt Up Button
		self.tiltupBtn = gtk.Button(stock=gtk.STOCK_GO_UP)
		self.tiltupBtn.connect("clicked", self.ptUp)
		self.table.attach(self.tiltupBtn, 1, 2, 0, 1)

		# Pan Left Button
		self.panleftBtn = gtk.Button(stock=gtk.STOCK_GO_BACK)
		self.panleftBtn.connect("clicked", self.ptLeft)
		self.table.attach(self.panleftBtn, 0, 1, 1, 2)

		# Pan/tilt Reset Button
		self.resetBtn = gtk.Button(stock=gtk.STOCK_UNDO)
		self.resetBtn.connect("clicked", self.ptReset)
		self.table.attach(self.resetBtn, 1, 2, 1, 2)

		# Pan Right Button
		self.panrightBtn = gtk.Button(stock=gtk.STOCK_GO_FORWARD)
		self.panrightBtn.connect("clicked", self.ptRight)
		self.table.attach(self.panrightBtn, 2, 3, 1, 2)

		# Tilt Down Button
		self.tiltdownBtn = gtk.Button(stock=gtk.STOCK_GO_DOWN)
		self.tiltdownBtn.connect("clicked", self.ptDown)
		self.table.attach(self.tiltdownBtn, 1, 2, 2, 3)

		# Quit Button
		self.quitBtn = gtk.Button(stock=gtk.STOCK_QUIT)
		self.quitBtn.connect("clicked", self.exit)
		self.table.attach(self.quitBtn, 1, 2, 4, 5)

		# Now display the table we built
		self.table.show()

		# Show the entire window
		window.show_all()

	
	## Now for the subfunctions required to actually do something for our app
	# Tilt up

	# Quit the application completely
	def exit(self, widget, data=None):
		gtk.main_quit()

	# Hide the window on certain events
	def hide(self, widget, button, window):
		if window.get_property ('visible'):
			window.hide()
		return window

	# Detect if window was minimized and hide
	def window_event(self, widget, event, window):
		if event.changed_mask & gtk.gdk.WINDOW_STATE_ICONIFIED:
			  if event.new_window_state & gtk.gdk.WINDOW_STATE_ICONIFIED:
			  	window.hide()
		return window

	# Show the popup menu
	def popup_menu(self, widget, button, time, sMenu = None):
		if sMenu:
			sMenu.show_all()
			sMenu.popup(None, None, None, 3, time)
		pass

	# Show the window if otherwise hidden, background, or minimized
	def activate_window(self, widget, window):
		if window.get_property ('visible'):
			window.present()
		else:
			window.show_all()
			window.deiconify()

def webcam_feed():
	print "Opening camera..."
	cap = cv.VideoCapture(1)
	
	while(True):
		# Capture frame-by-frame
		ret, frame = cap.read()
		cv.rectangle(frame, (270, 190), (370, 290), (0, 0, 255), 2)
		faces = faceCascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv.cv.CV_HAAR_SCALE_IMAGE)
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
				print "Pan ", "right" if correctionX < 0 else "left"
				pan(correctionX)
			if abs(correctionY)>160:
				print "Tilt ", "down" if correctionY < 0 else "up"
				tilt(correctionY)

			# if bestFaceCentreX not in range(imageCentreX-bestFace[2], imageCentreX+bestFace[2]):
			# 	correctionX = imageCentreX - bestFaceCentreX
			# 	#pan(correctionX)

			# if bestFaceCentreY not in range(imageCentreY-bestFace[2], imageCentreY+bestFace[2]):
			# 	correctionY = imageCentreY - bestFaceCentreY
			# 	#tilt(-correctionY)

		if ret:
			cv.imshow( 'Camera' , frame )
		if cv.waitKey(1) & 0xFF == ord('q'):
			break
	cap.release()
	cv.destroyAllWindows()

def tilt(value):
	control = "Tilt (relative)"
	result = subprocess.Popen([UVCDYNCTRLEXEC, "-d", deviceName, "-s", control, "--", str(value)]), 
	return True

def pan(value):
	control = "Pan (relative)"
	result = subprocess.Popen([UVCDYNCTRLEXEC, "-d", deviceName, "-s", control, "--", str(value)]), 
	return True


# Pan/Tilt Reset	
def ptReset(self, widget):
	control = "Pan/tilt Reset"
	value = "3"
	result = subprocess.Popen([UVCDYNCTRLEXEC, "-d", deviceName, "-s", control, value]), 
	return True

## Let's call our class and load all info
#ccUVCPTZ_Main()

webcam_feed()

## I don't think I need to worry about threads here??
#gtk.gdk.threads_init()

## Now let's run the init part of the script
#gtk.main()
