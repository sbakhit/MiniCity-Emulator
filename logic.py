import csv
import itertools
import random


class Grid():
    def __init__(self, size):
        self.grid = [[-1] * size] * size
    
    def populate(self, objs):
        for _, obj in objs.items():
            i, j = obj.loc
            self.grid[i][j] = obj.id

    def update(self, obj):
        i, j = obj.loc
        self.grid[i][j] = obj.id


class Fog():
    def __init__(self, location, radius, grid_size):
        self.loc = location
        self.radius = radius
        self.grid_size = grid_size

        self.points = self._gen_points()
        self.objects = set()

    def _gen_points(self):
        i_list = []
        j_list = []
        i, j = self.loc
        for x in range(-self.radius, self.radius + 1, 1):
            if (i + x) >= 0 and (i + x) < self.grid_size:
                i_list.append(i + x)
            if (j + x) >= 0 and (j + x) < self.grid_size:
                j_list.append(j + x)
        inputdata = [
            i_list,
            j_list
        ]
        return set(itertools.product(*inputdata))

    def update_loc(self, location):
        self.loc = location

    def update_radius(self, radius):
        self.radius = radius
        self.points = self._gen_points()

    def add_object(self, obj):
        self.object.add(obj)

    def remove_object(self, obj):
        self.object.remove(obj)


class Object():
    def __init__(self, pid, starting_location):
        self.id = pid
        self.starting_location = starting_location
        self.loc = starting_location

        self.connection = False
        self.fog = None
        self.routes = None

    def gen_routes(self, num_points):
        self.routes = [self.starting_location]

        for n in range(num_points):
            r = random.randrange(0, 2)
            i, j = self.routes[-1]
            self.routes.append((i + (1 - r), j + r))

    def connect(self):
        # TODO: connect to RPI using MQTT
        self.connection = True

    def send(self, data):
        # TODO: send to RPI
        return False


class Configuration():
    def __init__(self, path=None):
        self.path = path
        self.data = {}

    def update_path(self, path):
        self.path = path

    def parse(self):
        with open(self.path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            self.data = {}
            for idx, line in enumerate(reader):
                self.data[idx] = [pt for pt in line]

        print(self.data)