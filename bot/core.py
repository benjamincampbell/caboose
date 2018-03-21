import bot.command
import logging
import yaml
import time
import threading
import queue
import os

from .command import reload_commands
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
        self.CFG = self.read_config()

        bot.command.decorate_mans(self.LEADER, self.COMMANDS)

    def read_config(self):
        with open('config.yaml', 'r') as f:
            cfg = yaml.load(f)
            self.NICK = cfg['settings']['nick']
            self.LEADER = cfg['settings']['leader']
            self.NICKSERV_EMAIL = cfg['settings']['email']
            self.NICKSERV_PASS = cfg['settings']['pwd']
            self.API_KEYS = cfg['settings']['api_keys']
            self.create_connections(cfg)

        return cfg

    def update_config(self):
        os.remove('config.yaml')
        with open('config.yaml', 'w') as f:
            yaml.dump(self.CFG, f, default_flow_style=False)

    def create_connections(self, cfg):
        for name, settings in cfg['servers'].items():
            self.CONNECTIONS[name] = Connection(name, settings)

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
                            logging.info('{0}: {1} called {2} command with args: {3}'.format(line.conn.SERVER.HOST, line.user, line.command, line.text))
                            self.COMMANDS[line.command](self, line)
            line_queue.task_done()
