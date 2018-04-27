#!/usr/bin/env python

import cv2 as OpenCV
import time, requests, sys
from datetime import datetime

hostname = "vibe.hopto.org"
API_port = 24655
venue_ID = 1
sensorType = "camera"
camera_ID = 1
camera_port = 0 #on this computer, ie /dev/video${camera_port}

if (len(sys.argv) > 1):
	camera_port = int(sys.argv[1])
if (len(sys.argv) > 2):
	hostname = sys.argv[2]
if (len(sys.argv) > 3):
	venue_ID = sys.argv[3]
if (len(sys.argv) > 4):
	camera_ID = sys.argv[4]

camera = OpenCV.VideoCapture(camera_port)

upload_URL = "http://{0}:{1}/api/post/venue/{2}/{3}/{4}".format(
	hostname, API_port, venue_ID, sensorType, camera_ID
)

def SendPicture(filename, url = upload_URL):
	file = {'file': (open(filename, 'rb'))}
	response = requests.post(upload_URL, files = file, timeout = 2)
	return response

def WriteResponse(response):
	print("Got response: ", response, ".", sep="")
	print(response.text)

def SavePicture(frame):
	time = datetime.now()
	filename = 'pictures/picture_{:d}-{:02d}-{:02d}.png'.format(
		time.hour, time.minute, time.second
	)
	OpenCV.imwrite(filename, frame)
	return filename

def ConfirmSend(imageFile):
	print(datetime.now(), "picture", imageFile, "sent.")

def RejectSend():
	print(datetime.now(), "API didn't connect.")

timeBetweenSends = 4 #seconds
notDone = True

if not camera.isOpened():
	print("Could not open camera", camera_port)
	quit()

while notDone:
	notDone, image = camera.read()
	imageFile = SavePicture(image)
	try:
		response = SendPicture(imageFile)
		ConfirmSend(imageFile)
		WriteResponse(response)
	except requests.exceptions.ConnectionError:
		RejectSend()
	except requests.exceptions.ReadTimeout:
		print("send timeout")
	time.sleep(timeBetweenSends)
