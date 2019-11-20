import pandas as pd

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
        self.config_file = config_file

    def update_config_file(self, config_file):
        self.config_file = config_file

    def parse(self):
        if self.config_file == None:
            raise FileNotFoundError

        config = pd.from_csv('self.config_file', sep='\t', header=0)
        print(config)
