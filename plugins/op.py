@command("op", man = "Gives levels of ops to a user. -h to give half ops Usage: &ops [-h] user")
def op(nick, channel, message, handler):
	opstring = "+"
	count = 0
	for user in message.split():
            count += 1

    #We need one 'o' for each person we are giving ops, i.e. +ooo nick1 nick2 nick3
	for i in range(count):
            opstring += "o"
	opstring += " "
	for user in message.split():
            opstring += "%s " % user

	if (nick == handler.NICK) or (nick in handler.SETTINGS.globaladmins) :
		handler.sendraw("MODE %s %s\r\n" % (channel, opstring))
	else:
		handler.privmsg(channel, '{}: You don\'t have permission to do that'.format(nick))
