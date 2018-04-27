#!/usr/bin/env bash

HarryJunior="http://vibe.hopto.org:24655"
CAPACITY=20 # play with this if you want
VENUE_ID=1
URI_base=${HarryJunior}/api/post/venue/${VENUE_ID}
Capacity_URI=${URI_base}/capacity
Population_URI=${URI_base}/population

# # set capacity to CAPACITY
# curl ${Capacity_URI}/${CAPACITY}

# sleep 20 # seconds to wait before the script does anything else
# in this time you should restart the simulator 
# and set up the screen recording in QuickTime 

for number in $(seq 1 ${CAPACITY}); do
	curl ${Population_URI}/${number}
	sleep 1.5 # seconds.
	# You can modify this to modify the time between updates on the recording
done
