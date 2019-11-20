import csv

class Object():
    def __init__(self, weel_radius, speed):
        self.weel_radius = weel_radius
        self.speed = speed

        self.connection = False
    
    def connect(self):
        # TODO: connect to RPI using MQTT
        self.connection = True
    
    def send(self, data):
        # TODO: send to RPI
        return False


class Configuration():
    def __init__(self, config_file=None):
        self.path = config_file
        self.data = {}

    def update_config_file(self, config_file):
        self.path = config_file

    def parse(self):
        with open(self.path, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            next(reader)

            self.data = {}
            for idx, line in enumerate(reader):
                self.data[idx] = [pt for pt in line]

        print(self.data)