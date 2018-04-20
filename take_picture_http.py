#!/usr/bin/env python

import cv2 as OpenCV
from datetime import datetime
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
	filename = 'pictures/DSilvs_is_the_fucking_man.png'
	OpenCV.imwrite(filename, frame)
	return filename

frame_ms = 100
intervalCount = 0
oneMinute = 60 * 1000
framesPerMinute = oneMinute / frame_ms

if camera.isOpened(): # try to get the first frame
	rval, frame = camera.read()
else:
	rval = False

while rval:
	OpenCV.imshow("bar picture", frame)
	rval, frame = camera.read()
	key = OpenCV.waitKey(frame_ms)
	if key == ESC:
		break
	if (intervalCount == 0):
		imageFile = SavePicture(frame)
		try:
			response = SendPicture(imageFile)
			#WriteResponse(response)
		except requests.exceptions.ConnectionError:
			print("Shit didn't connect.")
	intervalCount += 1
	intervalCount %= framesPerMinute

OpenCV.destroyWindow("bar picture")

