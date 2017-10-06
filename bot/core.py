import sys
import socket
import bot.reload
import datetime
import logging

from . import reload
from .connection import Connection

class Bot:
    def __init__(self):
        self.NICK = ''
        self.LEADER = ''
        self.COMMANDS = reload_commands
        self.CONNECTIONS = {}
        self.ACTIVE = False
        
    def read_config(self):
        with open('config.yaml', 'r') as f:
            cfg = yaml.load(f)
            self.NICK = cfg['settings']['nick']
            self.LEADER = cfg['settings']['leader']
            for name, settings in self.config['servers'].items():
                self.CONNECTIONS[name] = Connection(settings)


    def make_connections(self, servers):
        """
        Make connections using the Server objects taken
        from the config.yaml file
        """
        
    def socket_connect(self, host, port):
        self.SOCK = socket.socket()
        print("Connecting to server: {0}".format(host))
        logging.info("Connecting to server: {0}")
        self.SOCK.connect((host, port))

    def recv(self):
        message = self.SOCK.recv(2048).decode("utf-8")
        return message

    def sendraw(self, string):
        print(">" + string.strip())
        self.SOCK.send(string.encode())

    def privmsg(self, channel, message):
        msg = "PRIVMSG %s :%s\r\n" % (channel, message)
        self.sendraw(msg)

    def password(self, pwd):
        """Sends password to IRC server"""
        self.sendraw("PASS %s\r\n" % pwd)

    def nick(self, nickname):
        """Set IRC nick"""
        self.sendraw("NICK %s\r\n" % nickname)

    def user(self, ident, name):
        """Set IRC user"""
        self.sendraw("USER %s 0 * :%s\r\n" % (ident, name))

    def join(self, chan):
        """Join IRC Channel"""
        self.sendraw("JOIN %s\r\n" % chan)

    def leave(self, chan):
        """Leave IRC Channel"""
        self.sendraw("PART %s\r\n" % chan)

    def pong(self, response):
        """Send PONG response to server PING"""
        self.sendraw("PONG %s\r\n" % response)

    def kick(self, channel, user, reason):
        """ Kick user from channel (if has ops)"""
        self.sendraw("KICK %s %s :%s\r\n" % (channel, user, reason))

    def listen(self):
        #Initial connect, set nick, user, and join channels
        self.socket_connect(self.HOST, self.PORT)
        self.nick(self.NICK)
        self.user(self.NICK, self.NICK)
        for channel in self.CHANNELS:
            self.join(channel)
            self.privmsg(channel, "{0} up and running".format(self.NICK))

        while 1:
            #The listen loop
            data = self.recv()
            for line in data.splitlines():
                    print(line)
                    if "PING" == line.split()[0]:
                        self.pong(line.split()[1])

                #Any other checks, such as userjoins, would go here
                    if "JOIN" == line.split()[1]:
                        #source JOIN :#channel
                        parts = data.split(sep = ' ', maxsplit = 2)
                        real_source, real_channel = parts[0], parts[2]
                        nick = real_source.split(sep = '!')[0][1:]
                        channel = line.split(sep = '#')[1]

                        if nick != self.NICK:
                            if self.CHANNELS["#" + channel].autoops:
                                self.COMMANDS['op'](self.NICK, "#" + channel, nick, self)
                            if self.CHANNELS["#" + channel].autovoice:
                                self.COMMANDS['voice'](self.NICK, "#" + channel, nick, self)
                            if self.CHANNELS["#" + channel].autokick:
                                self.kick("#" + channel, nick, self.SETTINGS.channels["#" + channel].autokick_message)

                    if "PRIVMSG" in line:
                        parts = data.split(sep=' ', maxsplit=3)
                        if len(parts) == 4:
                            #Raw parts of the original message
                            #source PRIVMSG target :message
                            real_source = parts[0]
                            real_target = parts[2]
                            real_message = parts[3]
    
                            #extract source user nickname
                            # :nick!user@host
                            nick = real_source.split(sep='!')[0][1:]
    
                            #if a user PRIVMSGes us we appear as the target
                            if real_target == self.NICK:
                                channel = nick
                            else:
                                channel = real_target
    
                            #Final parameter (message) is often prefixed with ':'
                            if real_message.startswith(':'):
                                message = real_message[1:]
                            else:
                                message = real_message
    
                            #Must answer the call of duty
                            if message.strip() == "bot roll call":
                                self.privmsg(channel, "My name is Michael J. Caboose and I hate babies.")
    
                            #Check if we care about the msesage
                            if message.startswith(self.LEADER):
                                parts = message.strip().split(sep=None, maxsplit=1)
                                command_ = parts[0][len(self.LEADER):]
                                #Give a default value for message if none is provided.
                                if len(parts) == 2:
                                    message = parts[1]
                                else:
                                    message = ""
                                
                                #invoke associated command or error
                                if command_ in self.COMMANDS:
                                    if (self.COMMANDS[command_].enabled and nick.lower() not in self.SETTINGS.ignore):
                                            self.COMMANDS[command_](nick, channel, message, self)
                                elif command_ == "reload":
                                    self.COMMANDS = bot.reload.reload_commands()
                                elif command_ == "source":
                                    self.privmsg(channel, "http://github.com/benjamincampbell/caboose")
