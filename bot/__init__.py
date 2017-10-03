import re

class Line(raw):
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
        self.user = UserInfo(raw.split(' ', 1)[0][1:])
        
        parse_line(raw.split(' ', 1)[1])
        
    
    def parse_line(raw):
        
        
class UserInfo:
    def __init__(self, raw_user):
        self.nick = None
        self.user = None
        self.host = None
        
    def parse_user(raw_user):
        match = re.search('^([^!]+)!([^@]+)@(.+)$', raw_user)
        if match: