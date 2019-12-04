import paho.mqtt.client as mqtt
import time
import csv

from helpers import assign_fog

def publish(world, cars, fogs, broker_url, broker_port):
    def on_connect(client, userdata, flags, rc):
        print('connection code {}'.format(rc))
        for topic in MQTT_PATHS:
            client.subscribe(topic + '/brain', qos=1)

    def on_message(client, userdata, msg):
        # get id, topic and object
        tmp = msg.topic.split('/')
        id_ = tmp[-2]

        topic = '/'.join(tmp[:-1])
        car = cars.get(id_)

        # update
        try:
            location = tuple(map(int, msg.payload.decode('ASCII').strip('(').strip(')').split(',')))
            world.reset(car)
            car.update_loc(location)
            world.update(car)
            assign_fog(fogs, car)

            assigned_fog = None
            if car.fog != None:
                assigned_fog = car.fog.id
            log_files[id_].write('{}\t{}\n'.format(location, assigned_fog))
        except ValueError:
            # initial start message
            pass

        if car.route:
            next_point = str(car.route.pop(0))
            client.publish(topic=topic, payload=next_point, qos=1, retain=False)
        else:
            car.connection = False
            client.unsubscribe(topic)
            client_ids.remove(id_)
            if(not client_ids):
                client.disconnect()

    client_ids = [id_ for id_ in cars.keys()]
    MQTT_PATHS = ['/car/' + id_ for id_ in client_ids]
    client = mqtt.Client("admin")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker_url, broker_port)

    log_files = {}
    for car_id, car in cars.items():
        log_files[car_id] = open('log/' + car_id, 'w+')
        log_files[car_id].write('{}\t{}\n'.format('location', 'fog'))
        fog_id = car.fog.id if car.fog else None
        log_files[car_id].write('{}\t{}\n'.format(car.starting_location, fog_id))

    # init process
    time.sleep(10)
    for topic in MQTT_PATHS:
        data = 'start'
        client.publish(topic=topic, payload=data, qos=1, retain=False)

    client.loop_forever()

    time.sleep(10)
    # close files
    for id_, f in log_files.items():
        f.close()


# command line script to start the process without the GUI
if __name__ == "__main__":
    import sys
    import os
    from logic import Grid, Fog, Object, Configuration
    from helpers import generate_fogs, generate_cars, assign_objects_fog, start_clients, stop_clients

    def run_script():
        '''
        - parse config file
        - connect
        '''
        print('parsing configuration file...')
        config.parse()
        broker_url = config.configdict["broker"]["url"]
        broker_port = config.configdict["broker"]["port"]
        width = config.configdict["dimensions"]["width"]
        height = config.configdict["dimensions"]["height"]

        print('Initializing world parameters')
        print('Creating grid...')
        world = Grid(width=width, height=height)

        print('Creating fogs...')
        fogs = generate_fogs(config.configdict["fogs"], width, height)

        print('Creating objects...')
        cars = generate_cars(config.configdict["objects"])

        print('Creating clients...')
        client_ids = [id_ for id_ in cars.keys()]
        clients = start_clients(client_ids, broker_url, broker_port)

        print('Populating world...')
        world.populate(cars)
        assign_objects_fog(fogs, cars)

        print('running..')
        for _, car in cars.items():
            car.connection = True
        publish(world, cars, fogs, broker_url, int(broker_port))

        print('DONE!')
        # kill client processes
        stop_clients(clients)

    #############START OF PROCESS#############
    if len(sys.argv) < 2:
        print('configuration file missing')
        exit(1)
    elif not os.path.isfile(sys.argv[1]):
        print('configuration file not found')
        exit(1)

    # world variables
    config = Configuration()
    config.update_path(sys.argv[1])

    run_script()
    #############END OF PROCESS#############