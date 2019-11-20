import sys
import math
import random
import subprocess

BROKER_URL = "localhost"
BROKER_PORT = 1883

WORLD_SIZE = 1024
NUM_POINTS = 5

from logic import Object

def assign_fog(fogs, obj):
    min_fog_dst = (sys.maxint, -1)
    min_dst, fog_idx = min_fog_dst

    x1, y1 = obj.loc
    for idx, fog in enumerate(fogs):
        x2, y2 = fog.loc
        dst = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

        if dst < min_dst:
            min_dst = dst
            fog_idx = idx

    if fog_idx < 0:
        if obj.fog != None:
            obj.fog.remove_object(obj)
            obj.fog = None
    elif obj.loc in fogs[fog_idx].points:
        fogs[fog_idx].add_object(obj)
        obj.fog = fogs[fog_idx]

def generate_routes_old(pids_list, num_points, grid_size):
    routes_dict = {}
    for idx, _ in enumerate(pids_list):
        routes_dict[idx] = []

    for obj, pts in routes_dict.items():
        for i in range(num_points):
            r = random.randrange(0, 2)
            i, j = pts[-1]
            pts.append((i + (1 - r), j + r))

    return routes_dict

def generate_objects(pids_list, grid_size):
    objects = {}
    for idx, _ in enumerate(pids_list):
        objects[idx] = Object(idx, (random.randrange(0, grid_size), random.randrange(0, grid_size)))
    return objects

def generate_routes(objects, num_points):
    routes_dict = {}
    for pid, obj in objects.items():
        obj.gen_routes(num_points)
        routes_dict[pid] = obj.route
    return routes_dict

def gen_routes(starting_location, num_points):
    routes = [starting_location]

    for n in range(num_points):
        r = random.randrange(0, 2)
        i, j = routes[-1]
        routes.append((i + (1 - r), j + r))

    return routes

def get_pids(name):
    pids = None
    while True:
        try:
            pids = subprocess.check_output(["pgrep", "-f", name]).decode('ASCII').split()
        except subprocess.CalledProcessError as e:
            print("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
            continue
        break
    return pids