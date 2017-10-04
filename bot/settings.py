import os.path
import yaml

class Settings:
    """
    Object to hold various global settings for Caboose
    """
    def __init__(self):
        self.globaladmins = []
        self.config = {}
        self.servers = {}
        self.update()

    def update(self):
        
        
    def update_ignorelist(self):
        

    def update_globaladminlist(self):


    def update_config(self):
        """
        Load in data from config.yaml
        """

class Channel:
    """
    Object to hold various channel-specific settings for Caboose
    """
    def __init__(self, name):
        self.name = name
        self.autoops = False
        self.autovoice = False
        self.autokick = False
        self.autokick_message = "I knew it. We're all going to die... Starting with you." #take from config file
        self.spamlimit = False
        self.admins = [] # Take from config file
        self.ignore = []
        
    def __str__(self):
        return self.name

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



class Server:
    """
    Holds information about each server that Caboose will be connected to
    """
    def __init__(self):
        self.HOST = None
        self.PORT = None
        self.PASS = None # will be left blank in config if no pass, so this will stay None
        self.SSL = None
        self.CONNECTED = None
        self.CHANNELS = {}
        