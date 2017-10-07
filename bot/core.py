import bot.reload
import logging
import yaml
import time

from .reload import reload_commands
from .connection import Connection
from .line import Line

class Bot:
    def __init__(self):
        self.NICK = ''
        self.LEADER = ''
        self.NICKSERV_EMAIL = ''
        self.NICKSERV_PASS = ''
        self.COMMANDS = reload_commands
        self.CONNECTIONS = {}
        
        self.read_config()
        
    def read_config(self):
        with open('config.yaml', 'r') as f:
            cfg = yaml.load(f)
            self.NICK = cfg['settings']['nick']
            self.LEADER = cfg['settings']['leader']
            self.NICKSERV_EMAIL = cfg['settings']['email']
            self.NICKSERV_PASS = cfg['settings']['pwd']
            for name, settings in cfg['servers'].items():
                self.CONNECTIONS[name] = Connection(settings)

    def listen(self):
        for name, conn in self.CONNECTIONS.items():
            logging.info("{0} initializing connection".format(conn))
            conn.socket_connect()
            if conn.SERVER.PASS:
                conn.pwd()
            conn.nick(self.NICK)
            conn.user(self.NICK, self.NICK)            
        
        # Caboose needs to wait until after it receives a MODE message
        # before these can be sent
 

        while 1:
            for name, conn in self.CONNECTIONS.items():
                if conn.MODE and not conn.POSTMODE:
                    if conn.SERVER.NICKSERV:
                            conn.nickserv_reg(self.NICKSERV_PASS, self.NICKSERV_EMAIL)
                            conn.nickserv_ident(self.NICKSERV_PASS)            
                    for key, chan in conn.SERVER.CHANNELS.items():
                        conn.join(chan)
                        conn.privmsg(chan, '{0} up and running.'.format(self.NICK))
                    conn.POSTMODE = True
                data = conn.recv()
                for l in data.splitlines():
                    line = Line(l)
                    line.parse_line(self.LEADER)
                    # print('{0} {1}'.format(conn, line))
                    if line.type == 'MODE':
                        conn.MODE = True
                    if line.type == 'PING':
                        conn.pong(line.text)
                    if line.type == 'PRIVMSG':       
                        if line.command:                                
                            # invoke associated command or error
                            if line.command in self.COMMANDS:
                                if (self.COMMANDS[command_].enabled and nick.lower() not in self.SETTINGS.ignore):
                                        self.COMMANDS[command_](nick, channel, message, self)
                            elif line.command == "reload":
                                conn.COMMANDS = bot.reload.reload_commands()
                            elif line.command == "source":
                                conn.privmsg(channel, "http://github.com/benjamincampbell/caboose")
