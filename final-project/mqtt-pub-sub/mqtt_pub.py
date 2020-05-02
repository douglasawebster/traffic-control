import paho.mqtt.client as mqtt
from datetime import datetime
from time import sleep
import sys
import requests
import json
import re

# The following code makes reference to code supplied by:
# https://github.com/eclipse/paho.mqtt.python/blob/master/examples/client_pub-wait.py

# To run this program: python3 mqtt_pub.py [token]
# token = the token supplied by flespi account

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))


def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))
    pass


def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mqttc, obj, level, string):
    print(string)

# The command line arg that contains the token necessary to connect to flespi
keys_file = sys.argv[1]
keys = json.load(open(keys_file, "r"))

username = keys["flespi"]
request_url = keys["tomtom"]

# The command line arg that contains the streetlight data
streetlight_data_file = sys.argv[2]
streetlights = json.load(open(streetlight_data_file, "r"))


mqttc = mqtt.Client()
mqttc.username_pw_set(username, password=None)
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

mqttc.connect("mqtt.flespi.io", 1883, 60)  # Connecting to flespi


# https://developer.tomtom.com/content/traffic-api-explorer#/Traffic%20Flow/get_traffic_services__versionNumber__flowSegmentData__style___zoom___format_
# https://developer.tomtom.com/content/traffic-api-explorer#/Traffic%20Flow/get_traffic_map__versionNumber__tile_flow__style___zoom___x___y___mimeType_
# https://developer.tomtom.com/blog/build-different/using-traffic-data-maps-and-routes

mqttc.loop_start()

# Queries traffic data given a coordinates and publishes data to to po181u/
while 1:

    time_stamp = now = datetime.now().strftime("%H:%M:%S")

    ctr = 0
    for streetlight_id in streetlights:

        if ctr < 5:
            ctr += 1
            streetlight = streetlights[streetlight_id]


            # Replaces latitude and longitude place holders in url with the streetlights coordinates
            request_url_with_coords = re.sub('\sLATITUDE\s', str(streetlight['latitude']), request_url)
            request_url_with_coords = re.sub('\sLONGITUDE\s', str(streetlight['longitude']), request_url_with_coords)

            # Request traffic data given coordinates
            traffic_request = requests.get(request_url_with_coords)
            json_object = traffic_request.json()

            data = json_object['flowSegmentData']
            message_payload = {
                "currentSpeed": data['currentSpeed'],
                "freeFlowSpeed": data['freeFlowSpeed'],
                "currentTravelTime": data['currentTravelTime'],
                "freeFlowTravelTime": data['freeFlowTravelTime'],
                "roadClosure": data['roadClosure'],
                "confidence": data['confidence'],
                "timeStamp": str(time_stamp)
            }

            topic = "po181u/final-project/traffic-data/" + streetlight_id
            print(topic)

            info = mqttc.publish(topic, json.dumps(message_payload) +"\n", qos=1)

    sleep(10)

infot.wait_for_publish()