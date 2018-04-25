#!/usr/bin/env python

import cv2 as OpenCV
from datetime import datetime, timedelta
import requests, sys, shutil

ESC = 27
ENTER = 13

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

OpenCV.namedWindow("live preview")
camera = OpenCV.VideoCapture(camera_port)

upload_URL = "http://{0}:{1}/api/post/venue/{2}/{3}/{4}".format(
	hostname, API_port, venue_ID, sensorType, camera_ID
)

def SendPicture(filename, url = upload_URL):
	file = {'file': (open(filename, 'rb'))}
	response = requests.post(upload_URL, files = file)
	return response

def ShowResponse(response):
	print("Got response: ", response, ".", sep="")
	if response.status_code == 200:
		content_type = response.headers.get('content-type')
		if content_type == 'image/jpeg':
			img = response.raw.read()
			pic = "response.jpg"
			with open(pic, 'wb') as f:
				for chunk in response:
					f.write(chunk)
			picToShow = OpenCV.imread(pic)
			OpenCV.imshow("Computer vision response", picToShow);
		else:
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

if camera.isOpened(): # try to get the first frame
	rval, frame = camera.read()
else:
	rval = False

frame_ms = 100

while rval:
	OpenCV.imshow("live preview", frame)
	rval, frame = camera.read()
	key = OpenCV.waitKey(frame_ms)
	if key == ESC:
		break
	if key == ENTER:
		imageFile = SavePicture(frame)
		try:
			response = SendPicture(imageFile)
			ConfirmSend(imageFile)
			ShowResponse(response)
		except requests.exceptions.ConnectionError:
			RejectSend()


OpenCV.destroyWindow("live preview")
