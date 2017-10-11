import bot.reload
import logging
import yaml
import time
import threading
import queue

from .reload import reload_commands
from .connection import Connection
from .line import Line

class Bot:
    def __init__(self):
        self.NICK = ''
        self.LEADER = ''
        self.NICKSERV_EMAIL = ''
        self.NICKSERV_PASS = ''
        self.COMMANDS = reload_commands()
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

    def run(self):
        line_queue = queue.Queue()
        threads = []
        
        for name, conn in self.CONNECTIONS.items():
            t = threading.Thread(target=conn.start, args=(self.NICK, line_queue)) 


        while 1:
            for name, conn in self.CONNECTIONS.items():
                data = conn.recv()
                for l in data.splitlines():
                    line = Line(l)
                    line.parse_line(self.LEADER)
                    # print('{0} {1}'.format(conn, line))
                    if line.type == 'MODE':
                        conn.initialize(self.NICKSERV_EMAIL, self.NICKSERV_PASS, self.NICK)
                    elif line.type == 'PING':
                        conn.pong(line.text)
                    elif line.type == 'PRIVMSG':       
                        if line.command:                                
                            # invoke associated command or error
                            if line.command in self.COMMANDS:
                                if (self.COMMANDS[command_].enabled and nick.lower() not in self.SETTINGS.ignore):
                                        self.COMMANDS[command_](nick, channel, message, self)
                            elif line.command == "reload":
                                conn.COMMANDS = bot.reload.reload_commands()
                            elif line.command == "source":
                                conn.privmsg(channel, "http://github.com/benjamincampbell/caboose")
