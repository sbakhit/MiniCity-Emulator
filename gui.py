import os
from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk

from logic import Configuration
from logic import Object


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        # input variables
        self.export_file = None
        self.config = Configuration()

        # initialize variables
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
        self.config.update_config_file(path)

    def export_data(self):
        self.export_file = filedialog.asksaveasfilename(initialdir=self.directory, title="Export Simulation Data",
                                                           filetypes=(("txt files", "*.txt"), ("tsv files", "*.tsv"),
                                                                      ("all files", "*.*")))

    def run_script(self):
        '''
        - parse config file
        - connect
        '''
        self.config.parse()
        print('running')
        for obj, pts in self.config.data.items():
            print(pts)
        print('done')


root = Tk() # create a Tk root window

root.geometry('512x512')

b = Window(root)

root.mainloop()