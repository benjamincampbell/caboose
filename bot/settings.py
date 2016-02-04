import configparser
import os.path

class settings:

    def __init__(self):
        self.ignore = []
        self.admins = []
        self.config = {}
        self.channels = {}
        self.update()

    def update(self):
        #Updates all at once, separate methods in case only one needs updating
        self.update_ignorelist()
        self.update_adminlist()
        self.update_config()
        
    def update_ignorelist(self):
        #Check and make sure a file is made if it doesn't exist
        if (os.path.exists("ignore.txt")) == False:
            with open("ignore.txt", 'w') as f:
                pass
        ignorelist = []
        with open("ignore.txt", 'r') as f:
            ignorelist = f.read().splitlines()
        self.ignore = ignorelist

    def update_adminlist(self):
        if (os.path.exists("admins.txt")) == False:
            with open("admins.txt", 'w') as f:
                pass
        adminlist = []
        with open("admins.txt", 'r') as f:
            adminlist = f.read().splitlines()
        self.admins = adminlist

    def update_config(self):
        #Uses configparser to load the config file
        dict1 = {}
        dict2 = {}
        Config = configparser.ConfigParser()
        Config.read("config.ini")
        options = Config.options("Settings")
        for option in options:
            if option != "channels":
                dict1[option] = Config.get("Settings", option)
            else:
                dict2[option] = []
                for channel in Config.get("Settings", option).split(','):
                    dict1[option].append("#{0}".format(channel))
        self.config = dict1
        self.channels = dict2