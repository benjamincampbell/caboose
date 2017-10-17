import unittest
import yaml

from bot.line import Line, UserInfo
from bot.connection import Server, Channel, Connection
from bot.core import Bot

class TestIrcLineParsing(unittest.TestCase):
    
    def test_normal_privmsg(self):
        l = Line('dummy conn', ':Twitch!twitch@hostname.com PRIVMSG #channel :Test response')
        l.parse_line('!')
        
        self.assertEqual(l.user.nick, 'Twitch')
        self.assertEqual(l.user.user, 'twitch')
        self.assertEqual(l.user.host, 'hostname.com')
        
        self.assertEqual(l.type, 'PRIVMSG')
        self.assertEqual(l.args, ['#channel'])
        self.assertEqual(l.command, None)
        self.assertEqual(l.text, 'Test response')
        
    def test_ping(self):
        l = Line('dummy conn', 'PING :irc.example.com')
        l.parse_line('!')
        
        self.assertEqual(l.type, 'PING')
        self.assertEqual(l.args, [])
        self.assertEqual(l.command, None)
        self.assertEqual(l.text, 'irc.example.com')
        
    def test_command_privmsg(self):
        l = Line('dummy conn', ':Twitch!twitch@hostname.com PRIVMSG #channel :!echo hello church')
        l.parse_line('!')
        
        self.assertEqual(l.user.nick, 'Twitch')
        self.assertEqual(l.user.user, 'twitch')
        self.assertEqual(l.user.host, 'hostname.com')
        
        self.assertEqual(l.type, 'PRIVMSG')
        self.assertEqual(l.args, ['#channel'])
        self.assertEqual(l.command, 'echo')
        self.assertEqual(l.text, 'hello church')
        
    def test_mode(self):
        l = Line('dummy conn', ':caboose MODE caboose :+iwxz')
        l.parse_line('!')
        
        self.assertEqual(l.type, 'MODE')
        
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
        nickserv: true
        admins:
          - twitch
        channels:
          - "#caboose"
        ignore: []
    test2:
        host: irc.testserver2.org
        port: 6667
        pwd: ~
        ssl: false
        nickserv: true
        admins:
          - notlikethesoup
        channels:
          - "#caboose"
        ignore: []
          """
        cfg = yaml.load(f)
        connections = {}
        
        nick = cfg['settings']['nick']
        leader = cfg['settings']['leader']
        
        for name, settings in cfg['servers'].items():
            connections[name] = Connection(name, settings)
            
        self.assertEqual(nick, 'caboose')
        self.assertEqual(leader, '!')
        
        self.assertEqual(connections['test1'].SERVER.NAME, 'test1')
        self.assertEqual(connections['test1'].SERVER.HOST, 'irc.testserver1.org')
        self.assertEqual(connections['test1'].SERVER.PORT, 42697)
        self.assertEqual(connections['test1'].SERVER.PASS, 'testpass')
        self.assertEqual(connections['test1'].SERVER.SSL, True)
        self.assertEqual(connections['test1'].SERVER.ADMINS, ['twitch'])
        
        self.assertEqual(connections['test2'].SERVER.NAME, 'test2')
        self.assertEqual(connections['test2'].SERVER.HOST, 'irc.testserver2.org')
        self.assertEqual(connections['test2'].SERVER.PORT, 6667)
        self.assertEqual(connections['test2'].SERVER.PASS, None)
        self.assertEqual(connections['test2'].SERVER.SSL, False)
        self.assertEqual(connections['test2'].SERVER.ADMINS, ['notlikethesoup'])
        
        
class TestBotInitialization(unittest.TestCase):
    
    def test_init(self):
        caboose = Bot()
        
        print(caboose.COMMANDS)
        
        
if __name__ == '__main__':
    unittest.main()