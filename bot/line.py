import re

class Line:
    """
    Object to represent a line from the IRC server. We pass in
    the raw data, and it will be decoded and created into a
    Line object containing the information about it.
    
    Sample: :Twitch!~twitch@hostname.com PRIVMSG #channel :Test response
    """
    
    def __init__(self, raw):
        self.type = None
        self.channel = None
        self.command = None
        self.text = None
        self.raw = raw
        self.user = UserInfo()
    
    def parse_line():
        if self.raw[0] == ':':

            self.user.parse_user(self.raw.split(' ', 1)[0][1:])
        
class UserInfo:
    def __init__(self):
        self.nick = None
        self.user = None
        self.host = None
         
    def __str__(self):
        return '{0}!{1}@{2}'.format(self.nick, self.user, self.host)
        
    def parse_user(raw_user):
        match = re.search('^([^!]+)!([^@]+)@(.+)$', raw_user)
        if match:
            self.nick = match.group(1)
            self.user = match.group(2)
            self.host = match.group(3)