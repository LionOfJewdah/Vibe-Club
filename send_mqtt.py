import paho.mqtt.publish as publish
import time
import sys

def SendMessage(host, payload, topic="demo/davids_pi"):
    print("Sending message {0} to host {1} under topic {2}".format(
        payload, host, topic)
    )
    publish.single(topic, payload, hostname=host)

host = sys.argv[1]
IFuckingFeelLikeIt = True
while IFuckingFeelLikeIt:
    SendMessage(host, '{"numberOfPeople": 5}')
    time.sleep(4)

