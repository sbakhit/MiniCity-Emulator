import sys
import math
import subprocess

from logic import Object, Fog

def assign_fog(fogs, obj):
    min_fog_dst = (sys.maxsize, -1)
    min_dst, fog_idx = min_fog_dst
    x1, y1 = obj.loc
    for idx, fog in enumerate(fogs):
        x2, y2 = fog.loc
        dst = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        if dst < min_dst:
            min_dst = dst
            fog_idx = idx
    if fog_idx < 0:
        # out of range
        if obj.fog != None:
            obj.fog.remove_object(obj)
        obj.fog = None
    else:
        # found fog
        if obj.fog != None and obj.fog != fogs[fog_idx]:
            obj.fog.remove_object(obj)
        fogs[fog_idx].add_object(obj)
        obj.fog = fogs[fog_idx]

def assign_objects_fog(fogs, objs):
    for _, obj in objs.items():
        assign_fog(fogs, obj)

def generate_fogs(fogs_list, grid_width, grid_height):
    fogs = []
    for fog in fogs_list:
        id_ = fog["id"]
        location = (fog["location"]["x"], fog["location"]["y"])
        radius = fog["radius"]
        fogs.append(Fog(id_, location, radius, width=grid_width, height=grid_height))
    return fogs

def generate_cars(cars_list):
    objects = {}
    for car in cars_list:
        id_ = car["id"]
        starting_location = (car["starting_location"]["x"], car["starting_location"]["y"])
        # extract route points
        route = []
        for point in car["route"]:
            route.append((point["x"], point["y"]))
        # create object
        objects[id_] = Object(id_, starting_location, route)
    return objects

def start_clients(client_ids, broker_url, broker_port):
    clients = []
    for id_ in client_ids:
        args = ["python3", "subscriber.py", id_, broker_url, broker_port]
        clients.append(subprocess.Popen(args))
    return clients

def stop_clients(clients):
    for client in clients:
        client.kill()