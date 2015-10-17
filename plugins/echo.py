def echo(nick, channel, message, privmsg):
    privmsg(channel, '{}'.format(message))