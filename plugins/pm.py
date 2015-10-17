def pm(nick, channel, message, privmsg):
	#!pm targetUser message
	targetUser = message.split()[0]
	pmessage = message.split(" ", 1)[1]
	privmsg(targetUser, '{}: {}'.format(nick, pmessage))