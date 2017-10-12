import bot.reload
import logging
import yaml
import time
import threading
import queue

from .reload import reload_commands
from .connection import Connection
from .line import Line

class Bot(object):
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
            t = threading.Thread(target=conn.start, args=(self.LEADER, self.NICK, line_queue))
            t.start()
            threads.append(t)

        while 1:
            line = line_queue.get()
            if line.type == 'MODE':
                line.conn.initialize(self.NICKSERV_EMAIL, self.NICKSERV_PASS, self.NICK)
            elif line.type == 'PING':
                line.conn.pong(line.text)
            elif line.type == 'PRIVMSG':       
                if line.command:                                
                    # invoke associated command or error
                    if line.command in self.COMMANDS:
                        if (self.COMMANDS[line.command].enabled):
                                self.COMMANDS[line.command](line)
                    elif line.command == "reload":
                        conn.COMMANDS = bot.reload.reload_commands()
                    elif line.command == "source":
                        conn.privmsg(channel, "http://github.com/benjamincampbell/caboose")
            line_queue.task_done()