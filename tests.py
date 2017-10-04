import unittest

from bot.line import Line, UserInfo

class TestIrcLineParsing(unittest.TestCase):
    
    def test_normal_privmsg(self):
        l = Line(':Twitch!twitch@hostname.com PRIVMSG #channel :Test response')
        l.parse_line()
        
        self.assertEqual(l.type, 'PRIVMSG')
        self.assertEqual(l.channel, '#channel')
        self.assertEqual(l.command, None)
        self.assertEqual(l.text, 'Test response')
        
        self.assertEqual(l.user.nick, 'Twitch')
        self.assertEqual(l.user.user, 'twitch')
        self.assertEqual(l.user.host, 'hostname.com')
        
if __name__ == '__main__':
    unittest.main()