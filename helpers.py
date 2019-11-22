import sys
import math
import random
import subprocess

BROKER_URL = "localhost"
BROKER_PORT = 1883

WORLD_SIZE = 1024
NUM_CLIENTS = 5
NUM_POINTS = 5
NUM_FOGS = 4

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
            obj.fog.re
            obj.fog = None


    if fog_idx < 0:
        if obj.fog != None:
            print('removing fog {} from object {}'.format(obj.fog.id, obj.id))
            obj.fog.remove_object(obj)
            obj.fog = None
    elif obj.loc in fogs[fog_idx].points:
        if obj.fog != None:
            print('removing fog {} from object {}'.format(obj.fog.id, obj.id))
            obj.fog.remove_object(obj)
            obj.fog = None
        print('adding fog {} to object {}'.format(fogs[fog_idx].id, obj.id))
        fogs[fog_idx].add_object(obj)
        obj.fog = fogs[fog_idx]
    else:
        obj.fog = None

def assign_objects_fog(fogs, objs):
    for _, obj in objs.items():
        assign_fog(fogs, obj)

# def generate_routes_old(pids_list, num_points, grid_size):
#     routes_dict = {}
#     for idx, _ in enumerate(pids_list):
#         routes_dict[idx] = []

#     for obj, pts in routes_dict.items():
#         for i in range(num_points):
#             r = random.randrange(0, 2)
#             i, j = pts[-1]
#             pts.append((i + (1 - r), j + r))

#     return routes_dict

def generate_fogs(count, grid_size):
    fogs = []
    for i in range(count):
        location = (random.randrange(0, grid_size), random.randrange(0, grid_size))
        radius = random.randrange(0, grid_size//4)
        fogs.append(Fog(location, radius, grid_size))
    return fogs
    

def generate_objects(client_ids, grid_size):
    objects = {}
    for _, id_ in enumerate(client_ids):
        objects[id_] = Object(id_, (random.randrange(0, grid_size), random.randrange(0, grid_size)))
    return objects

def generate_routes(objects, num_points):
    routes_dict = {}
    for id_, obj in objects.items():
        obj.generate_routes(num_points)
        routes_dict[id_] = obj.routes
    return routes_dict

# def generate_object_routes(obj, num_points):
#     routes = [obj.starting_location]
#     for n in range(num_points):
#         r = random.randrange(0, 2)
#         i, j = routes[-1]
#         routes.append((i + (1 - r), j + r))
#     return routes

# def gen_routes(starting_location, num_points):
#     routes = [starting_location]
#     for n in range(num_points):
#         r = random.randrange(0, 2)
#         i, j = routes[-1]
#         routes.append((i + (1 - r), j + r))
#     return routes

# def get_pids(name):
#     pids = None
#     while True:
#         try:
#             pids = subprocess.check_output(["pgrep", "-f", name]).decode('ASCII').split()
#         except subprocess.CalledProcessError as e:
#             print("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
#             continue
#         break
#     return pids

def start_clients(name, count):
    clients = []
    for i in range(count):
        clients.append(subprocess.Popen(['python3', name]))
    return clients

def stop_clients(clients):
    for client in clients:
        client.kill()