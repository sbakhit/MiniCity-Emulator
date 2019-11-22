import paho.mqtt.client as mqtt
import time
import os

from helpers import BROKER_URL, BROKER_PORT

pid = str(os.getpid())
MQTT_PATH = "/object/" + pid
MQTT_PATH_BRAIN = MQTT_PATH + '/brain'

def on_connect(client, userdata, flags, rc):
    print('process {} connection code {}'.format(pid, rc))
    client.subscribe(MQTT_PATH, qos=1)

def on_message(client, userdata, msg):
    # simulates driving
    time.sleep(5)
    client.publish(topic=MQTT_PATH_BRAIN, payload=msg.payload, qos=1, retain=False)

client = mqtt.Client(client_id=pid)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER_URL, BROKER_PORT)

client.loop_forever()