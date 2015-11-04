import sys
import socket
import bot.reload

class irc_handler:
    def __init__(self, host, port, nick, startchannels, leader, commands):
        self.HOST = host
        self.PORT = int(port)
        self.NICK = nick
        self.STARTCHANNELS = startchannels
        self.LEADER = leader
        self.COMMANDS = commands

    def socket_connect(self, host, port):
        self.SOCK = socket.socket()
        print("Connecting to server: {0}".format(host))
        self.SOCK.connect((host, port))

    def recv(self):
        try:
            message = self.SOCK.recv(2048).decode("utf-8")
        except:
            print("A BAD THING HAPPENED IN recv()")
        return message

    def sendraw(self, string):
        try:
            print(">" + string.strip())
            self.SOCK.send(string.encode())
        except:
            print("A BAD THING HAPPENED IN sendraw()")

    def privmsg(self, channel, message):
        msg = "PRIVMSG %s :%s\r\n" % (channel, message)
        self.sendraw(msg)

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
        self.sendraw("PONG %s\r\n" %response)

    def listen(self):
        self.socket_connect(self.HOST, self.PORT)
        self.nick(self.NICK)
        self.user(self.NICK, self.NICK)
        for channel in self.STARTCHANNELS:
            self.join(channel)
            self.privmsg(channel, "{0} up and running".format(self.NICK))

        while 1:
            data = self.recv()
            for line in data.splitlines():
                try:
                    print(line)
                except:
                    print("AN ERROR OCCURED IN print(line)")
                if "PING" == line.split()[0]:
                    self.pong(line.split()[1])
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
                            print(message)
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
                                self.COMMANDS[command_](nick, channel, message, self)
                            elif command_ == "reload":
                                self.COMMANDS = bot.reload.reload_commands()
                            elif command_ == "source":
                                self.privmsg(channel, "http://github.com/benjamincampbell/caboose")
                            else:
                                self.privmsg(channel, "unknown command '{}'".format(command_))