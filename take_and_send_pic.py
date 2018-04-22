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
venue_ID = 1
sensorType = "camera"
camera_ID = 1

if (len(sys.argv) > 1):
	hostname = sys.argv[1]
if (len(sys.argv) > 2):
	venue_ID = sys.argv[2]

upload_URL = "http://{0}:{1}/api/post/venue/{2}/{3}?sensor_ID={4}".format(
	hostname, API_port, venue_ID, sensorType, camera_ID
)

def SendPicture(filename, url = upload_URL):
	file = {'file': (open(filename, 'rb'))}
	response = requests.post(upload_URL, files = file)
	return response

def WriteResponse(response):
	print("Got response: ", response, ".", sep="")
	#print(response.text)

def SavePicture(frame):
	time = datetime.now()
	filename = 'pictures/DSilvs_{:d}:{:02d}:{:02d}.png'.format(
		time.hour, time.minute, time.second
	)
	OpenCV.imwrite(filename, frame)
	return filename

def ConfirmSend(imageFile):
	print(datetime.now(), "picture", imageFile, "sent.")

def RejectSend():
	print(datetime.now(), "API didn't connect.")

if camera.isOpened(): # try to get the first frame
	rval, frame = camera.read()
else:
	rval = False

frame_ms = 250
haventSentThisMinute = True
firstTime = datetime.now()
sendPeriod = timedelta(seconds = 60)
fiveSecondWindow = timedelta(seconds = 5)

while rval:
	OpenCV.imshow("bar picture", frame)
	rval, frame = camera.read()
	key = OpenCV.waitKey(frame_ms)
	if key == ESC:
		break
	difference = (datetime.now() - firstTime) % sendPeriod
	if (difference < fiveSecondWindow):
		if haventSentThisMinute:
			imageFile = SavePicture(frame)
			try:
				response = SendPicture(imageFile)
				ConfirmSend(imageFile)
				WriteResponse(response)
			except requests.exceptions.ConnectionError:
				RejectSend()
			haventSentThisMinute = False
	else:
		haventSentThisMinute = True

OpenCV.destroyWindow("bar picture")
