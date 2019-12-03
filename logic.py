import itertools
import random
import json


class Grid():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[-1] * width] * height

    def populate(self, objects):
        for _, obj in objects.items():
            i, j = obj.loc
            self.grid[i][j] = obj.id

    def reset(self, obj):
        i, j = obj.loc
        self.grid[i][j] = -1

    def update(self, obj):
        i, j = obj.loc
        self.grid[i][j] = obj.id


class Fog():
    def __init__(self, id_, location, radius, width, height):
        self.id = id_
        self.loc = location
        self.radius = radius
        self.width = width
        self.height = height

        self.points = self._gen_points()
        self.objects = set()

    def _gen_points(self):
        i_list = []
        j_list = []
        i, j = self.loc
        for x in range(-self.radius, self.radius + 1, 1):
            if (i + x) >= 0 and (i + x) < self.height:
                i_list.append(i + x)
            if (j + x) >= 0 and (j + x) < self.width:
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
        self.objects.add(obj)

    def remove_object(self, obj):
        self.objects.remove(obj)


class Object():
    def __init__(self, id_, starting_location, route=None, stationary=False):
        self.id = id_
        self.starting_location = starting_location
        self.loc = starting_location

        self.route = route
        self.connection = False
        self.fog = None

    def update_loc(self, location):
        self.loc = location


class Configuration():
    def __init__(self, path=None):
        self.path = path
        self.configdict = {}

    def update_path(self, path):
        self.path = path

    def parse(self):
        with open(self.path, "r") as json_file:
            self.configdict = json.load(json_file)

        dimensions = self.configdict["dimensions"]
        fogs = self.configdict["fogs"]
        cars = self.configdict["cars"]
        print('world dimensions: width = {}, height = {}'.format(dimensions["width"], dimensions["height"]))