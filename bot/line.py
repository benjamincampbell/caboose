import re
import collections 

class Line:
    """
    Object to represent a line from the IRC server. We pass in
    the raw data, and it will be decoded and created into a
    Line object containing the information about it.
    
    Sample: :Twitch!twitch@hostname.com PRIVMSG #channel :Test response
            :Twitch!twitch@hostname.com PRIVMSG #channel :!echo hello
    """
    
    def __init__(self, raw):
        self.type = None
        self.command = None
        self.args = []
        self.text = ''
        self.raw = raw
        self.user = UserInfo()
        
    def __str__(self):
        return self.raw
    
    def parse_line(self, leader):
        print(self.raw)
        parts = collections.deque(self.raw.strip().split(' '))
        try:
            if parts[0][0] == ':':
                self.user.parse_user(parts.popleft()[1:])
        except IndexError:
            logging.warning('Problem parsing line, parts: {0}'.format(parts))
        if parts:
            self.type = parts.popleft()
        
        txt = []
        message = False
        for p in parts:
            if not message:
                if p[0] == ':':
                    message = True
                    if p[1] == leader:
                        self.command = p.strip()[2:]
                    else:
                        txt.append(p.strip()[1:])
                else:
                    self.args.append(p.strip())
            else:
                txt.append(p.strip())
        self.text = ' '.join(txt)
        
        
class UserInfo:
    """
    Object to hold the nick, user, and host information of a Line
    """
    def __init__(self):
        self.nick = None
        self.user = None
        self.host = None
         
    def __str__(self):
        return '{0}!{1}@{2}'.format(self.nick, self.user, self.host)
        
    def parse_user(self, raw_user):
        match = re.search('^([^!]+)!([^@]+)@(.+)$', raw_user)
        if match:
            self.nick = match.group(1)
            self.user = match.group(2)
            self.host = match.group(3)