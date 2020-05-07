import paho.mqtt.client as mqtt
import sys
import json


# The following code makes reference to code supplied by:
# https://github.com/eclipse/paho.mqtt.python/blob/master/examples/client_sub.py

# To run this program: python3 mqtt_sub.py [token]
# token = the token supplied by flespi account

def on_connect(mqttc, obj, flags, rc):
    print("rc: " + str(rc))

def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)

# The command line arg that contains the token necessary to connect to flespi
file = sys.argv[1]
keys = json.load(open(file, "r"))

username = keys["flespi"]

mqttc = mqtt.Client()
mqttc.username_pw_set(username, password=None)
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe

mqttc.connect("mqtt.flespi.io", 1883, 60)  # Connecting to flespi
mqttc.subscribe("united-states/california/san-diego-county/san-diego/la-jolla/#", 1)  # Subscribing to messages with topic = united-states/california/san-diego-county/san-diego/la-jolla/

mqttc.loop_forever()