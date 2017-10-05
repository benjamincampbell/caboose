import unittest
import yaml
import pprint

from bot.line import Line, UserInfo
from bot.settings import Settings, Server, Channel

class TestIrcLineParsing(unittest.TestCase):
    
    def test_normal_privmsg(self):
        l = Line(':Twitch!twitch@hostname.com PRIVMSG #channel :Test response')
        l.parse_line()
        
        self.assertEqual(l.type, 'PRIVMSG')
        self.assertEqual(l.args, ['#channel'])
        self.assertEqual(l.command, None)
        self.assertEqual(l.text, 'Test response')
        
        self.assertEqual(l.user.nick, 'Twitch')
        self.assertEqual(l.user.user, 'twitch')
        self.assertEqual(l.user.host, 'hostname.com')
        
    def test_ping(self):
        l = Line('PING :irc.example.com')
        l.parse_line()
        
        self.assertEqual(l.type, 'PING')
        self.assertEqual(l.args, [])
        self.assertEqual(l.command, None)
        self.assertEqual(l.text, 'irc.example.com')
        
class TestReadingConfig(unittest.TestCase):
    def test_reading_yaml(self):
        f = """settings:
    nick: caboose
    leader: "!"
connections:
    valinor:
        host: valinor.worf.co
        port: 42697
        pwd: connectpw1
        ssl: true
        admins:
          - twitch
        channels:
          - "#caboose"
    snoonet:
        host: irc.snoonet.org
        port: 6667
        pwd: ~
        ssl: false
        admins:
          - notlikethesoup
        channels:
          - "#caboose" """
        cfg = yaml.load(f)
        servers = {}
        
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(cfg)
        
        for name, settings in cfg['connections'].items():
            server = Server(name, **settings)
        
        pp.pprint(vars(server))
        
if __name__ == '__main__':
    unittest.main()