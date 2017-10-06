import unittest
import yaml

from bot.line import Line, UserInfo
from bot.connection import Server, Channel, Connection

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
        f = """
settings:
    nick: caboose
    leader: "!"
servers:
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
          - "#caboose"
          """
        cfg = yaml.load(f)
        connections = {}
        
        nick = cfg['settings']['nick']
        leader = cfg['settings']['leader']
        
        for name, settings in cfg['servers'].items():
            connections[name] = Connection(settings)
            
        self.assertEqual(nick, 'caboose')
        self.assertEqual(leader, '!')
            
        self.assertEqual(connections['test1'].SERVER.HOST, 'irc.testserver1.org')
        self.assertEqual(connections['test1'].SERVER.PORT, 42697)
        self.assertEqual(connections['test1'].SERVER.PASS, 'testpass')
        self.assertEqual(connections['test1'].SERVER.SSL, True)
        self.assertEqual(connections['test1'].SERVER.ADMINS, ['twitch'])
        
        self.assertEqual(connections['test2'].SERVER.HOST, 'irc.testserver2.org')
        self.assertEqual(connections['test2'].SERVER.PORT, 6667)
        self.assertEqual(connections['test2'].SERVER.PASS, None)
        self.assertEqual(connections['test2'].SERVER.SSL, False)
        self.assertEqual(connections['test2'].SERVER.ADMINS, ['notlikethesoup'])
        
        
if __name__ == '__main__':
    unittest.main()