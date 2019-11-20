import os

try:
    import tkFileDialog as filedialog
    py3 = 0
except ImportError:
    from tkinter import filedialog
    py3 = 1

try:
    from Tkinter import *
    py3 = 0
except ImportError:
    from tkinter import *
    py3 = 1

try:
    import ttk
    py3 = 0
except ImportError:
    import tkinter.ttk as ttk
    py3 = 1

from logic import Configuration
from logic import Object


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        # input variables
        self.config_file = None
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
        self.config_file = filedialog.askopenfilename(initialdir=self.directory, title="Select Configuration File",
                                                  filetypes=(("all files", "*.*"), ("tsv files", "*.tsv"),
                                                             ("csv files", "*.csv"), ("txt files", "*.txt")))
        self.config.update_config_file(self.config_file)

    def export_data(self):
        self.export_file = filedialog.asksaveasfilename(initialdir=self.directory, title="Export Simulation Data",
                                                           filetypes=(("txt files", "*.txt"), ("tsv files", "*.tsv"),
                                                                      ("all files", "*.*")))

    def run_script(self):
        '''
        - parse config file
        - connect
        '''
        print('running')


root = Tk()     # create a Tk root window

root.geometry('512x512')

b = Window(root)

root.mainloop()