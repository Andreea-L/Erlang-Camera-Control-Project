import cv2 as cv
import numpy as np
from PIL import Image
import glob
import re

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

i = 1

print glob.glob('Input/*.jpg')
for filename in natural_sort(glob.glob('*.jpg')):
	im=Image.open(filename).convert('RGB')
	open_cv_im = np.array(im) 
	open_cv_im = open_cv_im[:, :, ::-1].copy() 
	# Convert RGB to BGR 
	j=1
	faces = np.empty((1,0))
	while j<5 and (faces==() or faces.size==0):

		faceCascade = cv.CascadeClassifier("/home/andreea/Documents/catkin_ws/src/rosorbitcamera/src/HaarClassifiers/haarcascade_frontalface_"+str(j)+".xml")
		faces = faceCascade.detectMultiScale(open_cv_im, scaleFactor=1.1, minNeighbors=6, minSize=(50, 50), flags=cv.cv.CV_HAAR_SCALE_IMAGE)
		j+=1

	# if faces==() or faces.size==0:
	# 	backupCascade = cv.CascadeClassifier("/home/andreea/Documents/catkin_ws/src/rosorbitcamera/src/HaarClassifiers/haarcascade_frontalface_1.xml")
	# 	faces = backupCascade.detectMultiScale(open_cv_im, scaleFactor=1.1, minNeighbors=6, minSize=(50, 50), maxSize=(250, 250), flags=cv.cv.CV_HAAR_SCALE_IMAGE)

	bestFace = []
	if faces != () and faces.size > 0:		# OpenCv strangely returns empty tuples occasionally, so check for that
		bestFace = max(faces, key=lambda item:item[2])

	start_coord = (0,0)
	end_coord = (0,0)
	if bestFace!= []:
		start_coord = (bestFace[0], bestFace[1])
		end_coord = (bestFace[0]+bestFace[2], bestFace[1]+bestFace[3])
		cv.rectangle(open_cv_im, (bestFace[0], bestFace[1]), (bestFace[0]+bestFace[2], bestFace[1]+bestFace[3]), (255, 0, 0), 2)

	res_file = open("../Faces/face.coord","a+")
	res_file.write("ACTUAL:"+str(start_coord[0])+" "+str(start_coord[1])+" "+str(end_coord[0])+" "+str(end_coord[1])+"\n")
	res_file.close()
	ret = cv.imwrite("../Faces/"+filename+"face.jpg",open_cv_im)
	
	i+=1
	print ret