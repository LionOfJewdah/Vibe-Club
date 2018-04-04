import paho.mqtt.publish as publish
import time
import sys
from sched import scheduler
from datetime import datetime
from array import array

JSON_template = """{{
	\"numberOfPeople\": {0}
}}"""

venue_ID = 1
camera_ID = 1
sensorType = "camera"
myTopic = "vibe/venue_{0}/{1}_{2}".format(venue_ID, sensorType, camera_ID)

def SendMessage(host, payload, topic = myTopic):
	print("Sending message \"{0}\" to host {1} under topic '{2}'".format(
		payload, host, topic)
	)
	publish.single(topic, payload, hostname = host)

def SendPopulationCount(host, json_src, count, topic = myTopic):
	SendMessage(host, json_src.format(count), topic)

if (len (sys.argv) > 1):
	host = sys.argv[1]
else:
	host = "localhost"

populations = array('H', [4, 4, 5, 6, 6, 5, 6, 5, 5, 4, 3, 4])
populationCount = 4
timer = scheduler(time.time, time.sleep)
def PeriodicSend(task, it):
	populationCount = populations[it]
	SendPopulationCount(host, JSON_template, populationCount)
	it = int((it + 1) % (60 / 5))
	timer.enter(5, 1, PeriodicSend, (task, it,))

timer.enter(0, 1, PeriodicSend, (timer, 0))
timer.run()
