#!/usr/bin/env python

import cv2 as OpenCV
from datetime import datetime
from sched import scheduler
import requests

OpenCV.namedWindow("preview")
vc = OpenCV.VideoCapture(0)

ESC = 27
ENTER = 13

hostname = "localhost"
API_port = 8000
venue_ID = 2
sensorType = "camera"
camera_ID = 1
upload_URL = "http://{0}:{1}/api/post/venue/{2}/{3}?sensor_ID={4}".format(
	hostname, API_port, venue_ID, sensorType, camera_ID
)

def SendPicture(filename, url = upload_URL):
	file = {'file': (open(filename, 'rb'))}
	response = requests.post(upload_URL, files = file)
	return response

def WriteResponse(response):
	print("Got response: ", response, ".", sep="")
	fd = open("response.xml", "w")
	fd.write(response.text)
	fd.close()

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
	key = OpenCV.waitKey(2000)
	imageFile = SavePicture(frame)
	if key == ESC:
		break
	else:
		response = SendPicture(imageFile)
		WriteResponse(response)


OpenCV.destroyWindow("preview")

