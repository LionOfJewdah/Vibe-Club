#!/usr/bin/env python

import cv2 as OpenCV
from datetime import datetime, timedelta
from sched import scheduler
import requests, sys

OpenCV.namedWindow("bar picture")
camera = OpenCV.VideoCapture(0)

ESC = 27
ENTER = 13

hostname = "localhost"
API_port = 24655
venue_ID = 3
sensorType = "camera"
camera_ID = 1

if (len(sys.argv) > 1):
	hostname = sys.argv[1]

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
	filename = 'pictures/DSilvs.png'
	OpenCV.imwrite(filename, frame)
	return filename

if camera.isOpened(): # try to get the first frame
	rval, frame = camera.read()
else:
	rval = False

frame_ms = 200
haventSentThisMinute = True
firstTime = datetime.now()
oneMinute = timedelta(seconds = 60)
fiveSecondWindow = timedelta(seconds = 5)

while rval:
	OpenCV.imshow("bar picture", frame)
	rval, frame = camera.read()
	key = OpenCV.waitKey(frame_ms)
	if key == ESC:
		break
	difference = (datetime.now() - firstTime) % oneMinute
	if (difference < fiveSecondWindow):
		if haventSentThisMinute:
			imageFile = SavePicture(frame)
			try:
				response = SendPicture(imageFile)
				print(datetime.now(), "picture", imageFile, "sent.")
				#WriteResponse(response)
			except requests.exceptions.ConnectionError:
				print(datetime.now(), "API didn't connect.")
			haventSentThisMinute = False
	else:
		haventSentThisMinute = True

OpenCV.destroyWindow("bar picture")

