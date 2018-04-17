#!/usr/bin/env python
import requests, sys
from pathlib import Path
home = str(Path.home())

hostname = "localhost"
API_port = 8000
venue_ID = 3
sensorType = "camera"
camera_ID = 1
upload_URL = "http://{0}:{1}/api/post/venue/{2}/{3}?sensor_ID={4}".format(
	hostname, API_port, venue_ID, sensorType, camera_ID
)
picToSend = '{0}/computer_vision/images/t13.jpg'.format(home)

def SendPicture(filename, url = upload_URL):
	files = {'file': (open(filename, 'rb'))}
	response = requests.post(upload_URL, files = files)
	return response

def WriteResponse(response):
	print("Got response: ", response, ".", sep="")
	fd = open("response.xml", "w")
	fd.write(response.text)
	fd.close()

if (len (sys.argv) > 1):
	picToSend = sys.argv[1]
	if (len (sys.argv) > 2):
		picToSend2 = sys.argv[2]

response = SendPicture(picToSend)
WriteResponse(response)
