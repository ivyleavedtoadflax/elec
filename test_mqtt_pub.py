'''
Read a blinking LED and log
'''

#!/usr/bin/env python

import os
from time import strftime, sleep, time
from sendelec import sendElec, on_connect, on_publish
import paho.mqtt.client as mqtt
from paho.mqtt.publish import single

MQTT_HOST = os.environ.get('MQTT_HOST')
MQTT_PORT = int(os.environ.get('MQTT_PORT'))
MQTT_USERNAME = os.environ.get('MQTT_USERNAME')
MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD')
MQTT_TOPIC = os.environ.get('MQTT_TOPIC')

# Define callbacks

def on_connect(client, userdata, flags, rc):
    """
    Callback following connection to MQTT server
    """
    client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)

    print("Connected with result code " + str(rc))

def on_publish(client, userdata, result):
    """
    Callback following message receipt by server
    """
    print('Published to mqtt broker')

client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish

client.connect(host=MQTT_HOST, port=MQTT_PORT)
client.loop_start()
client.publish(topic="test", payload="Testing raspberry pi", qos=1)
client.loop_stop()
client.disconnect

single(
    topic=MQTT_TOPIC, payload="Testing", qos=1,
    hostname=MQTT_HOSTNAME, port=MQTT_PORT,
    auth={'username':MQTT_USERNAME, 'password':MQTT_PASSWORD}
    )
