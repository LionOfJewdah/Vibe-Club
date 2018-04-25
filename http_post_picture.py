#!/usr/bin/env python
import requests, sys
from pathlib import Path

hostname = "vibe.hopto.org"
API_port = 24655
venue_ID = 1
sensorType = "camera"
camera_ID = 1
picToSend = ""

if (len(sys.argv) > 1):
	picToSend = sys.argv[1]
	if (len(sys.argv) > 2):
		hostname = sys.argv[2]
		if (len(sys.argv) > 3):
			venue_ID = sys.argv[3]
			if (len(sys.argv) > 4):
				camera_ID = sys.argv[4]
else:
	home = str(Path.home())
	picToSend = '{0}/computer_vision/images/LavaLab 03 07.jpg'.format(home)

upload_URL = "http://{0}:{1}/api/post/venue/{2}/{3}/{4}".format(
	hostname, API_port, venue_ID, sensorType, camera_ID
)

def SendPicture(filename, url = upload_URL):
	files = {'file': (open(filename, 'rb'))}
	response = requests.post(upload_URL, files = files)
	return response

def WriteResponse(response):
	print("Got response: ", response, ".", sep="")
	print(response.text)
	# fd = open("response.xml", "w")
	# fd.write(response.text)
	# fd.close()


response = SendPicture(picToSend)
WriteResponse(response)
