import paho.mqtt.client as mqtt
import time

from helpers import WORLD_SIZE, NUM_POINTS, BROKER_URL, BROKER_PORT
from helpers import start_clients, stop_clients, generate_routes, generate_objects, assign_fog, assign_objects_fog
from logic import Grid, Fog, Object, Configuration

def on_connect(client, userdata, flags, rc):
    print('connection code {}'.format(rc))
    for topic in MQTT_PATHS:
        client.subscribe(topic + '/brain', qos=1)

def on_unsubscribe(client, userdata, mid):
    print('brain unsubscribed: {}'.format(mid))

def on_disconnect(client, userdata, rc):
    print('brain is disconnected: {}'.format(rc))

def on_message(client, userdata, msg):
    print('{} {}'.format(msg.topic, msg.payload))

    # get id, topic and object
    tmp = msg.topic.split('/')
    id_ = tmp[-2]

    topic = '/'.join(tmp[:-1])
    obj = objects.get(id_)

    # update
    try:
        location = tuple(map(int, msg.payload.decode('ASCII').strip('(').strip(')').split(',')))
        world.reset(obj)
        obj.update_loc(location)
        world.update(obj)
        assign_fog(fogs, obj)
    except ValueError:
        # initial start message
        pass

    if obj.routes:
        next_point = str(obj.routes.pop(0))
        client.publish(topic=topic, payload=next_point, qos=1, retain=False)
    else:
        client.unsubscribe(topic)
        client_ids.remove(id_)
        if(not client_ids):
            client.disconnect()

# step 0: create grid, fogs
world = Grid(WORLD_SIZE)
fogs = [
    Fog((0, 768), 128, WORLD_SIZE),
    Fog((256, 256), 128, WORLD_SIZE),
    Fog((512, 768), 128, WORLD_SIZE),
    Fog((768, 256), 128, WORLD_SIZE)
]

# step 1: start clients processes
clients = start_clients('subscriber.py', 4)
client_ids = [str(client.pid) for client in clients]

# step 2: create objects and routes
objects = generate_objects(client_ids, WORLD_SIZE)
routes = generate_routes(objects, NUM_POINTS)

# step 3: populate grid and fogs
world.populate(objects)
assign_objects_fog(fogs, objects)

# step 4: start process
MQTT_PATHS = ['/object/' + str(id_) for id_ in client_ids]
client = mqtt.Client("admin")
client.on_connect = on_connect
client.on_message = on_message
client.on_unsubscribe = on_unsubscribe
client.connect(BROKER_URL, BROKER_PORT)

# init process
time.sleep(5)
for topic in MQTT_PATHS:
    data = 'start'
    client.publish(topic=topic, payload=data, qos=1, retain=False)

client.loop_forever()

# kill client processes
stop_clients(clients)
print('DONE!')