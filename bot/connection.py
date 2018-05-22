import ssl
import socket
import logging
from .line import Line

class Connection(object):
    """
    Represents a connection to a server
    """

    def __init__(self, name, settings):
        self.SOCK = None
        self.SERVER = Server(name, **settings)
        self.CONNECTED = False

    def __str__(self):
        return '{0}:{1} -'.format(self.SERVER.HOST, self.SERVER.PORT)

    def socket_connect(self):
        """
        Create socket connection to given host and port
        """
        self.SOCK = socket.socket()
        if self.SERVER.SSL:
            self.SOCK = ssl.wrap_socket(self.SOCK)
        logging.info("{0} connecting to server".format(self))
        self.SOCK.connect((self.SERVER.HOST, self.SERVER.PORT))
        self.CONNECTED = True

    def socket_disconnect(self):
        self.SOCK = None
        print("Disconnecting from server: {0}".format(self.SERVER.HOST))
        logging.info("Disconnecting from server: {0}".format(self.SERVER.HOST))
        self.CONNECTED = False

    def start(self, leader, nickname, line_queue):
            self.socket_connect()
            if self.SERVER.PASS:
                self.pwd()
            self.nick(nickname)
            self.user(nickname, nickname)

            while True:
                data = self.recv()
                for l in data.splitlines():
                    logging.info('{}'.format(l))
                    line = Line(self, l)
                    line.parse_line(leader)
                    line_queue.put(line)

    def recv(self):
        """
        Receive data and return it
        """
        message = self.SOCK.recv(2048).decode("utf-8")
        return message

    def sendraw(self, string):
        """
        Send information to server
        """
        logging.info("{0} sendraw: {1}".format(self, string.encode()))
        self.SOCK.send('{}\r\n'.format(string).encode())

    def pwd(self):
        """
        Give password to server, if required
        """
        self.sendraw("PASS %s" % self.SERVER.PASS)

    def nick(self, nick):
        """
        Specify bot's nick on the server
        """
        self.sendraw("NICK %s" % nick)

    def user(self, nick, user):
        """
        Specify bot's user on the server
        """
        self.sendraw("USER %s 0 * :%s" % (nick, user))

    def privmsg(self, channel, message):
        """
        Send a PRIVMSG to server, used for most responses to commands
        """
        msg = "PRIVMSG %s :%s" % (channel, message)
        self.sendraw(msg)

    def join(self, chan):
        """
        Join IRC channel
        """
        self.sendraw("JOIN %s" % chan)

    def leave(self, chan):
        """
        Leave IRC Channel
        """
        self.sendraw("PART %s" % chan)

    def pong(self, response):
        """
        Respond to PING from server
        """
        print("PONG :%s" % response)
        self.sendraw("PONG :%s" % response)

    def kick(self, channel, user, reason):
        """
        Kick user from channel with reason
        """
        self.sendraw("KICK %s %s :%s" % (channel, user, reason))

    def initialize(self, nickserv_email, nickserv_pass, nick):
        if self.SERVER.NICKSERV:
            self.nickserv_ident(nickserv_pass)
        for key, chan in self.SERVER.CHANNELS.items():
            self.join(chan)

    def nickserv_ident(self, pwd):
        """
        Sends a message to identify with Nickserv
        """
        self.privmsg('nickserv', 'IDENTIFY {0}'.format(pwd))

class Server(object):
    """
    Holds information about each server that Caboose will be connected to
    """
    def __init__(self, name, host, port, pwd, ssl, nickserv, admins, channels, ignore):
        self.NAME = name
        self.HOST = host
        self.PORT = port
        self.PASS = pwd # will be left blank in config if no pass, so this will be None
        self.SSL = ssl
        self.NICKSERV = nickserv
        self.ADMINS = admins
        self.CHANNELS = {}
        self.IGNORE = ignore

        for channel in channels:
            self.CHANNELS[channel] = Channel(channel)

    def __str__(self):
        return self.NAME


class Channel(object):
    """
    Object to hold various channel-specific settings for Caboose
    """
    def __init__(self, name):
        self.name = name
        self.autoops = False
        self.autovoice = False
        self.spamlimit = False
        self.mods = []

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
