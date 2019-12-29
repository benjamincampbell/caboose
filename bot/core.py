import logging
import yaml
import time
import threading
import queue
import os
import sys
import traceback

import bot.command
from .db import get_db, create_tables
from .command import reload_commands
from .connection import Connection
from .line import Line

from googleapiclient.discovery import build
from PyDictionary import PyDictionary

class Bot(object):
    def __init__(self):
        self.NICK = ''
        self.LEADER = ''
        self.NICKSERV_EMAIL = ''
        self.NICKSERV_PASS = ''
        self.DB_CONN = get_db()
        self.COMMANDS, self.tables = reload_commands()
        self.SECRETS = []
        self.CONNECTIONS = {}
        self.CFG = self.read_config()

        create_tables(self, self.tables)

        self.setup_google()
        self.setup_pydictionary()

        bot.command.decorate_mans(self.LEADER, self.COMMANDS)

    def read_config(self):
        with open('config.yaml', 'r') as f:
            cfg = yaml.load(f)
            self.NICK = cfg['settings']['nick']
            self.LEADER = cfg['settings']['leader']
            self.NICKSERV_EMAIL = cfg['settings']['email']
            self.NICKSERV_PASS = cfg['settings']['pwd']
            self.SECRETS = cfg['settings']['secrets']
            self.create_connections(cfg)

        return cfg

    def update_config(self):
        os.remove('config.yaml')
        with open('config.yaml', 'w') as f:
            yaml.dump(self.CFG, f, default_flow_style=False)

    def create_connections(self, cfg):
        for name, settings in cfg['servers'].items():
            self.CONNECTIONS[name] = Connection(name, settings)

    def setup_google(self):
        self.google_search_service = build("customsearch", "v1",
            developerKey=self.SECRETS["api_keys"]["google"])
        #self.google_urlshortener_service = build("urlshortener", "v1",
            #developerKey=self.SECRETS["api_keys"]["google"])

    def setup_pydictionary(self):
        self.dictionary = PyDictionary()

    def run(self):
        line_queue = queue.Queue()
        threads = []

        for name, conn in self.CONNECTIONS.items():
            t = threading.Thread(target=conn.start, args=(self.LEADER, self.NICK, line_queue))
            t.start()
            threads.append(t)

        while 1:
            try:
                line = line_queue.get()
                if line.type == 'MODE':
                    line.conn.initialize(self.NICKSERV_EMAIL, self.NICKSERV_PASS, self.NICK)
                elif line.type == 'PING':
                    line.conn.pong(line.text)
                elif line.type == 'PRIVMSG':
                    if line.command:
                        # invoke associated command or error
                        if (line.command in self.COMMANDS):
                            if (self.COMMANDS[line.command].enabled):
                                logger = logging.getLogger("log")
                                logger.info("{0}: {1} called {2} command with args: {3}".format(line.conn.SERVER.HOST, line.user, line.command, line.text))
                                if (line.args[0] == self.NICK):
                                    line.args[0] = line.user.nick

                                self.COMMANDS[line.command](self, line)

                line_queue.task_done()
            except Exception as err:
                logger = logging.getLogger("log")
                logger.exception("Would've encountered fatal error")
