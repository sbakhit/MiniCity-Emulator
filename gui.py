import os
import threading

from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk

from logic import Grid, Fog, Object, Configuration
from helpers import generate_fogs, generate_cars, assign_objects_fog, start_clients, stop_clients

from publisher import publish


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        # world variables
        self.config = Configuration()
        self.world = None
        self.fogs = None
        self.cars = None

        # initialize variables
        self.export_file = None
        self.directory = os.getcwd()

        # create window
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title('Mini-City Emulator')
        self.create_menu()
        # self.user_input()

    def create_menu(self):
        menu = Menu(self.master)
        self.master.config(menu=menu)

        sub_menu_file = Menu(menu)
        menu.add_cascade(label='File', menu=sub_menu_file)

        sub_menu_file.add_command(label='Load', command=self.load_config)
        sub_menu_file.add_command(label='Run', command=self.run_script)
        sub_menu_file.add_command(label='Export', command=self.export_data)
        sub_menu_file.add_separator()
        sub_menu_file.add_command(label='Exit', command=quit)

    def load_config(self):
        path = filedialog.askopenfilename(initialdir=self.directory, title="Select Configuration File",
                                                  filetypes=(("all files", "*.*"), ("tsv files", "*.tsv"),
                                                             ("csv files", "*.csv"), ("txt files", "*.txt")))
        self.config.update_path(path)

    def export_data(self):
        self.export_file = filedialog.asksaveasfilename(initialdir=self.directory, title="Export Simulation Data",
                                                           filetypes=(("txt files", "*.txt"), ("tsv files", "*.tsv"),
                                                                      ("all files", "*.*")))

    def run_script(self):
        '''
        - parse config file
        - connect
        '''
        print('parsing configuration file...')
        self.config.parse()
        broker_url = self.config.configdict["broker"]["url"]
        broker_port = self.config.configdict["broker"]["port"]
        width = self.config.configdict["dimensions"]["width"]
        height = self.config.configdict["dimensions"]["height"]

        print('Initializing world parameters')
        print('Creating grid...')
        self.world = Grid(width=width, height=height)

        print('Creating fogs...')
        self.fogs = generate_fogs(self.config.configdict["fogs"], width, height)

        print('Creating objects...')
        self.cars = generate_cars(self.config.configdict["cars"])

        print('Creating clients...')
        client_ids = [id_ for id_ in self.cars.keys()]
        clients = start_clients(client_ids, broker_url, broker_port)

        print('Populating world...')
        self.world.populate(self.cars)
        assign_objects_fog(self.fogs, self.cars)

        print('running..')
        publisher_thread = threading.Thread(target=publish, args=(self.world, self.cars, self.fogs, broker_url, int(broker_port)))
        publisher_thread.start()
        publisher_thread.join()

        # connection_status = []
        # for _, car in self.cars.items():
        #     car.connection = True
        #     connection_status.append(True)
        
        # while True in connection_status:
        #     connection_status = []
        #     for car_id, car in self.cars.items():
        #         fog_id = car.fog.id if car.fog else -1
        #         print(car_id, car.loc, fog_id, car.connection)

        #         connection_status.append(car.connection)

        print('DONE!')
        # kill client processes
        stop_clients(clients)


root = Tk() # create a Tk root window

root.geometry('512x512')

b = Window(root)

root.mainloop()