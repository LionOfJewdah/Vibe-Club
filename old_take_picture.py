#!/usr/bin/env python

import pygame.camera as cameras
import pygame.image as image
from datetime import datetime
from sched import scheduler
import paho.mqtt as mqtt
#import base64
#import json


cameras.init()
camera = cameras.Camera(cameras.list_cameras()[0])
camera.start()

venue_ID = 2
sensorType = "camera"
camera_ID = 1
myTopic = "vibe/venue_{0}/{1}_{2}".format(venue_ID, sensorType, camera_ID)
host = "localhost"
port = 1883
period = 10 #seconds
mqtt_qos = 1

def TakePic():
	filename = 'webcam/thot_{0}.png'.format(str(datetime.now()))
	pic = camera.get_image()
	image.save(pic, filename)
	return filename

def SendPic(filename, host = host, topic = myTopic, port = port, qos = mqtt_qos):
	return

def TakePictureAndSend(host = host, topic = myTopic, port = port, qos = mqtt_qos):
	pic = TakePic()
	SendPic(pic, host, topic, port, qos)


timer = scheduler(time.time, time.sleep)

def PeriodictSend(task):
	TakePictureAndSend(host, myTopic, port, mqtt_qos)
	timer.enter(period, 1, PeriodicSend, (task, )) #timer.enter(seconds, priority, task, (params))
try:
	timer.enter(0, 1, PeriodicSend, (timer, ))
	timer.run()
finally:
	cameras.quit()
