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
