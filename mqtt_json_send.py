#!/usr/bin/env python

import paho.mqtt.publish as publish
import time
import sys
from sched import scheduler
from datetime import datetime
from array import array

JSON_template = """{{
	\"numberOfPeople\": {0}
}}"""

venue_ID = 3
camera_ID = 1
sensorType = "camera"
myTopic = "vibe/venue_{0}/{1}_{2}".format(venue_ID, sensorType, camera_ID)

def SendMessage(host, port, payload, topic = myTopic):
	print("Sending message \"{0}\" to host {1}:{2} under topic '{3}'".format(
		payload, host, port, topic)
	)
	publish.single(topic, payload, port = port, hostname = host)

def SendPopulationCount(host, port, json_src, count, topic = myTopic):
	SendMessage(host, port, json_src.format(count), topic)

host = "localhost"
port = 1883

if (len (sys.argv) > 1):
	host = sys.argv[1]
	if (len (sys.argv) > 2):
		port = int(sys.argv[2])


populations = array('H', [110, 111, 108, 105, 103, 101, 99, 102, 104, 106, 109, 111])
populationCount = 110
timer = scheduler(time.time, time.sleep)
def PeriodicSend(task, it):
	populationCount = populations[it]
	SendPopulationCount(host, port, JSON_template, populationCount)
	it = int((it + 1) % len(populations))
	timer.enter(8, 1, PeriodicSend, (task, it,)) #timer.enter(seconds, priority, task, (params))

timer.enter(0, 1, PeriodicSend, (timer, 0))
timer.run()
