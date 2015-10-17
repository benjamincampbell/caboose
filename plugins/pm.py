def pm(nick, channel, message, handler):
	#!pm targetUser message
	targetUser = message.split()[0]
	pmessage = message.split(" ", 1)[1]
	handler.privmsg(targetUser, '{}: {}'.format(nick, pmessage))