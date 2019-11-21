import paho.mqtt.client as mqtt

from helpers import WORLD_SIZE, NUM_POINTS, BROKER_URL, BROKER_PORT
from helpers import get_pids, generate_routes, generate_objects
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

    tmp = msg.topic.split('/')
    pid = tmp[-2]

    topic = '/'.join(tmp[:-1])
    obj = objects.get(pid)

    if obj.routes:
        next_point = str(obj.routes.pop(0))
        client.publish(topic=topic, payload=next_point, qos=1, retain=False)
    else:
        client.unsubscribe(topic)
        pids.remove(pid)
        if(not pids):
            client.disconnect()

# step 0: create grid, fogs
world = Grid(WORLD_SIZE)
fogs = [
    Fog((0, 768), 128, WORLD_SIZE),
    Fog((256, 256), 128, WORLD_SIZE),
    Fog((512, 768), 128, WORLD_SIZE),
    Fog((768, 256), 128, WORLD_SIZE)
]

# step 1: get all running subscribers
pids = get_pids('subscriber.py')

# step 2: create objects and routes
objects = generate_objects(pids, WORLD_SIZE)
routes = generate_routes(objects, NUM_POINTS)
print(routes)

# step 3: populate grid
world.populate(objects)
# populate fogs

# step 4: 
MQTT_PATHS = ['/object/' + str(pid) for pid in pids]
client = mqtt.Client("admin")
client.on_connect = on_connect
client.on_message = on_message
client.on_unsubscribe = on_unsubscribe
client.connect(BROKER_URL, BROKER_PORT)

# init process
for topic in MQTT_PATHS:
    data = 'start'
    client.publish(topic=topic, payload=data, qos=1, retain=False)

client.loop_forever()

print('DONE!')