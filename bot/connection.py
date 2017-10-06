import socket

class Connection:
    """
    Represents a connection to a server
    """
    def __init__(self, settings):
        self.SOCK = None
        self.SERVER = Server(**settings)
        self.CONNECTED = False
        
    def socket_connect(self, host, port):
        """
        Create socket connection to given host and port
        """
        self.SOCK = socket.socket()
        self.SOCK.connect((host, port))
        
    def sendraw(self, string):
        """
        Send information to server
        """
        self.SOCK.send(string.encode())
    
    def pwd(self):
        """
        Give password to server, if required
        """
        pass
    
    def nick(self, nick):
        """
        Specify bot's nick on the server
        """
        pass
    
    def user(self, nick, user):
        """
        Specify bot's user on the server
        """
        pass
    
    def recv(self):
        """
        Receive data and return it
        """
        pass
    
    def privmsg(self, channel, message):
        """
        Send a PRIVMSG to server, used for most responses to commands
        """
        pass
    
    def join(self, chan):
        """
        Join IRC channel
        """
        pass
    
    def leave(self, chan):
        """
        Leave IRC Channel
        """
        pass
    
    def pong(self, response):
        """
        Respond to PING from server
        """
        pass
    
    def kick(self, channel, user, reason):
        """
        Kick user from channel with reason
        """
        pass
    
class Server:
    """
    Holds information about each server that Caboose will be connected to
    """
    def __init__(self, host, port, pwd, ssl, admins, channels):
        self.HOST = host
        self.PORT = port
        self.PASS = pwd # will be left blank in config if no pass, so this will be None
        self.SSL = ssl
        self.ADMINS = admins
        self.CHANNELS = {}
        
        for channel in channels:
            self.CHANNELS[channel] = Channel(channel)
        

class Channel:
    """
    Object to hold various channel-specific settings for Caboose
    """
    def __init__(self, name):
        self.name = name
        self.autoops = False
        self.autovoice = False
        self.spamlimit = False
        self.mods = []
        self.ignore = []
        
    def __str__(self):
        return self.name

    def toggle_autoops(self):
        if (self.autoops):
            self.autoops = False
        else:
            self.autoops = True
        return self.autoops

    def toggle_autovoice(self):
        if (self.autovoice):
            self.autovoice = False
        else:
            self.autovoice = True
        return self.autovoice

    def toggle_spamlimit(self):
        if (self.spamlimit):
            self.spamlimit = False
        else:
            self.spamlimit = True
        return self.spamlimit

    def add_mod(self, mod):
        if mod in self.mods:
            return False
        else:
            self.mods.append(mod)
            return True

    def remove_mod(self, mod):
        if mod in self.mods:
            self.mods.remove(mod)
            return True
        else:
            return False