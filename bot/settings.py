import configparser

class settings:

    def __init__(self):
        self.ignore = []
        self.admins = []
        self.config = {}
        self.update()

    def update(self):
        self.ignore = self.get_ignorelist()
        self.admins = self.get_adminlist()
        self.config = self.get_config()

    def get_ignorelist(self):
        ignorelist = []
        with open("ignore.txt", 'r') as f:
            ignorelist = f.read().splitlines()
        return ignorelist

    def get_adminlist(self):
        adminlist = []
        with open("admins.txt", 'r') as f:
            adminlist = f.read().splitlines()
        return adminlist


    def get_config(self):
        #Uses configparser to load the config file
        dict1 = {}
        Config = configparser.ConfigParser()
        Config.read("config.ini")
        options = Config.options("Settings")
        for option in options:
            if option != "startchannels":
                dict1[option] = Config.get("Settings", option)
            else:
                dict1[option] = []
                for channel in Config.get("Settings", option).split(','):
                    dict1[option].append("#{0}".format(channel))
        return dict1