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
    def test_reading_correct_yaml(self):
        f = """settings:
    nick: caboose
    leader: "!"
connections:
    test1:
        host: irc.testserver1.org
        port: 42697
        pwd: testpass
        ssl: true
        admins:
          - twitch
        channels:
          - "#caboose"
    test2:
        host: irc.testserver2.org
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
            servers[name] = Server(name, **settings)
            pp.pprint(vars(servers[name]))
            
        self.assertEqual(servers['test1'].NAME, 'test1')
        self.assertEqual(servers['test1'].HOST, 'irc.testserver1.org')
        self.assertEqual(servers['test1'].PORT, 42697)
        self.assertEqual(servers['test1'].PASS, 'testpass')
        self.assertEqual(servers['test1'].SSL, True)
        self.assertEqual(servers['test1'].ADMINS, ['twitch'])
        self.assertEqual(servers['test1'].CHANNELS, ['#caboose'])
        
        self.assertEqual(servers['test2'].NAME, 'test2')
        self.assertEqual(servers['test2'].HOST, 'irc.testserver2.org')
        self.assertEqual(servers['test2'].PORT, 6667)
        self.assertEqual(servers['test2'].PASS, None)
        self.assertEqual(servers['test2'].SSL, False)
        self.assertEqual(servers['test2'].ADMINS, ['notlikethesoup'])
        self.assertEqual(servers['test2'].CHANNELS, ['#caboose'])
        
        
if __name__ == '__main__':
    unittest.main()