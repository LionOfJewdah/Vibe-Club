#!/usr/bin/env python
import cv2 as OpenCV
from datetime import datetime
from sched import scheduler
import paho.mqtt as mqtt

OpenCV.namedWindow("preview")
vc = OpenCV.VideoCapture(0)

ESC = 27
ENTER = 13

def SavePicture(frame):
	filename = 'pictures/pic_{0}.png'.format(str(datetime.now()))
    OpenCV.imwrite(filename, frame)
    return filename

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
	OpenCV.imshow("preview", frame)
	rval, frame = vc.read()
	key = OpenCV.waitKey(20)
	if key == ESC:
		break
	if key == ENTER:
		filename = SavePicture(frame)
		

OpenCV.destroyWindow("preview")


