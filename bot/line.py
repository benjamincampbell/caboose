import re
import collections
import logging

class Line:
    """
    Object to represent a line from the IRC server. We pass in
    the raw data, and it will be decoded and created into a
    Line object containing the information about it.

    Sample: :Twitch!twitch@hostname.com PRIVMSG #channel :Test response
            :Twitch!twitch@hostname.com PRIVMSG #channel :!echo hello
    """


    def __init__(self, conn, raw):
        self.conn = conn
        self.type = None
        self.command = None
        self.args = []
        self.text = ''
        self.raw = raw
        self.user = UserInfo()
        self.link_match = None
        # link_match should be such that:
        #     link_match.group(0) is the entire match
        #     link_match.group(1) is text prior to the link
        #     link_match.group(2) is the protocol
        #     link_match.group(3) is the host
        #     link_match.group(4) is the specific page in the host
        #     link_match.group(5) is text after the link

    def __str__(self):
        return self.raw
    
    def reply(self, text):
        # shorthand function to respond in the channel that the line originated from
        self.conn.privmsg(self.args[0], text)

    def parse_line(self, leader):

        LINK_REGEX = "(.*)(http|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])(.*)"

        logger = logging.getLogger("log")
        logger.info(self.raw)
        parts = collections.deque(self.raw.strip().split(' '))
        try:
            if parts[0][0] == ':':
                self.user.parse_user(parts.popleft()[1:])
        except IndexError:
            logger.warning('Problem parsing line, parts: {0}'.format(parts))
        if parts:
            self.type = parts.popleft()

        txt = []
        message = False
        for p in parts:
            if not message:
                try:
                    if p[0] == ':':
                        message = True
                        try:
                            if p[1] in leader:
                                self.command = p.strip()[2:]
                            else:

                                txt.append(p.strip()[1:])
                        except IndexError:
                            pass
                    else:
                        self.args.append(p.strip())
                except:
                    pass
            else:
                txt.append(p.strip())
        self.text = ' '.join(txt)
        
        # check for links
        match = re.search(LINK_REGEX, self.text)
        if match:
            self.link_match = match


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
