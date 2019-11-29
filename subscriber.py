import paho.mqtt.client as mqtt
import sys

id_ = sys.argv[1]
BROKER_URL = sys.argv[2]
BROKER_PORT = int(sys.argv[3])

MQTT_PATH = "/car/" + id_
MQTT_PATH_BRAIN = MQTT_PATH + '/brain'

def on_connect(client, userdata, flags, rc):
    print('process {} connection code {}'.format(id_, rc))
    client.subscribe(MQTT_PATH, qos=1)

def on_unsubscribe(client, userdata, mid):
    print('object unsubscribed: {}'.format(mid))
    client.disconnect()

def on_disconnect(client, userdata, rc):
    print('object is disconnected: {}'.format(rc))

def on_message(client, userdata, msg):
    # simulates driving
    client.publish(topic=MQTT_PATH_BRAIN, payload=msg.payload, qos=1, retain=False)

client = mqtt.Client(client_id=id_)
client.on_connect = on_connect
client.on_message = on_message
client.on_unsubscribe = on_unsubscribe
client.on_disconnect = on_disconnect
client.connect(BROKER_URL, BROKER_PORT)

client.loop_forever()