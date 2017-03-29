import configparser
import os.path

class ChannelOptions:
    #object to hold options on a by-channel basis
    def __init__(self):
        #set options to defaults
        self.autoops = False
        self.autovoice = False
        self.autokick = False
        self.autokick_message = "I knew it. We're all going to die. Starting with you."
        self.spamlimit = False
        self.admins = ['twitch']

    def toggle_autoops(self):
        if (self.autoops):
            self.autoops = False
            return False
        else:
            self.autoops = True
            return True

    def toggle_autovoice(self):
        if (self.autovoice):
            self.autovoice = False
            return False
        else:
            self.autovoice = True
            return True
        
    def toggle_autokick(self):
        if (self.autokick):
            self.autokick = False
            return False
        else:
            self.autokick = True
            return True

    def toggle_spamlimit(self):
        if (self.spamlimit):
            self.spamlimit = False
            return False
        else:
            self.spamlimit = True
            return True

    def add_admin(self, admin):
        if admin in self.admins:
            return False
        else:
            self.admins.append(admin)
            return True

    def remove_admin(self, admin):
        if admin in self.admins:
            self.admins.remove(admin)
            return True
        else:
            return False


class Settings:
    #object to hold settings for Caboose
    def __init__(self):
        self.ignore = []
        self.globaladmins = []
        self.config = {}
        self.channels = {}
        self.update()

    def update(self):
        #Updates all at once, separate methods in case only one needs updating
        self.update_ignorelist()
        self.update_globaladminlist()
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

    def update_globaladminlist(self):
        if (os.path.exists("globaladmins.txt")) == False:
            with open("globaladmins.txt", 'w') as f:
                pass
        adminlist = []
        with open("globaladmins.txt", 'r') as f:
            adminlist = f.read().splitlines()
        self.globaladmins = adminlist

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
                for channel in Config.get("Settings", option).split(','):
                    dict2["#" + channel] = ChannelOptions()
        self.config = dict1
        self.channels = dict2
