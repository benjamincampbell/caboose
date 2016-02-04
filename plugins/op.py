@command("op", man = "Gives levels of ops to a user. -h to give half ops Usage: &ops [-h] user")
def op(nick, channel, message, handler):
	if nick in handler.SETTINGS.admins:
		handler.sendraw("MODE %s +o %s\r\n" % (channel, nick))
	else:
		handler.privmsg(channel, '{}: You don\'t have permission to do that'.format(nick))
