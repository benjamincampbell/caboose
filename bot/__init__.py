

class Line(raw):
    """
    Object to represent a line from the IRC server. We pass in
    the raw data, and it will be decoded and created into a
    Line object containing the information about it.
    
    Sample: :Twitch!~twitch@hostname.com PRIVMSG #channel :Test response
    """
    
    def __init__(self):
        self.nick = None
        self.user = None
        self.host = None
        self.type = None
        self.channel = None
        
class UserInfo:
    def __init__(self):
        self.nick = None
        self.user = None
        self.host = None
        
        