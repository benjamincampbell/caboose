@command("op", man = "Gives levels of ops to a user. -h to give half ops Usage: &ops [-h] user")
def op(nick, channel, message, handler):
	opstring = "+"

	opstring += "o" for user in message.split()
	opstring += " "
	opstring += "%s " % user for user in message.split()

	if nick in handler.SETTINGS.admins:
		handler.sendraw("MODE %s %s\r\n" % (channel, opstring))
	else:
		handler.privmsg(channel, '{}: You don\'t have permission to do that'.format(nick))
