import paho.mqtt.client as mqtt
import time
import csv

from helpers import WORLD_SIZE, NUM_POINTS, BROKER_URL, BROKER_PORT, NUM_FOGS, NUM_CLIENTS
from helpers import start_clients, stop_clients, generate_routes, generate_objects, assign_fog, assign_objects_fog, generate_fogs
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

        assigned_fog = None
        if obj.fog != None:
            assigned_fog = obj.fog.id
        log_files[id_].write('{}\t{}\n'.format(location, assigned_fog))
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
fogs = generate_fogs(NUM_FOGS, WORLD_SIZE)
# fogs = [
#     Fog((0, 768), 128, WORLD_SIZE),
#     Fog((256, 256), 128, WORLD_SIZE),
#     Fog((512, 768), 128, WORLD_SIZE),
#     Fog((768, 256), 128, WORLD_SIZE)
# ]

# step 1: start clients processes
clients = start_clients('subscriber.py', NUM_CLIENTS)
client_ids = [str(client.pid) for client in clients]

# step 2: create objects and routes
objects = generate_objects(client_ids, WORLD_SIZE)
routes = generate_routes(objects, NUM_POINTS)

# step 3: populate grid and fogs
world.populate(objects)
assign_objects_fog(fogs, objects)

# step 4: start process
MQTT_PATHS = ['/object/' + id_ for id_ in client_ids]
client = mqtt.Client("admin")
client.on_connect = on_connect
client.on_message = on_message
client.on_unsubscribe = on_unsubscribe
client.connect(BROKER_URL, BROKER_PORT)

# step 5: create log files
with open('log/config.tsv', 'w') as configFile:
    headers = '\t'.join(['p{}'.format(i) for i in range(len(routes))])
    configFile.write('id\t{}\n'.format(headers))
    for id_, route in routes.items():
        line = id_
        for p in route:
            line += '\t' + str(p)
        configFile.write(line + '\n')

log_files = {}
for id_, route in routes.items():
    log_files[id_] = open('log/' + id_, 'w+')
    log_files[id_].write('{}\t{}\n'.format('location', 'fog'))

# step 6: init process
time.sleep(10)
for topic in MQTT_PATHS:
    data = 'start'
    client.publish(topic=topic, payload=data, qos=1, retain=False)

client.loop_forever()

time.sleep(10)
# close files
for id_, f in log_files.items():
    f.close()

# kill client processes
stop_clients(clients)
print('DONE!')