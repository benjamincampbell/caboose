def echo(nick, channel, message, handler):
    handler.privmsg(channel, '{}'.format(message))