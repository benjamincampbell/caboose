@command("op", man = "Gives levels of ops to a user. -h to give half ops Usage: {leader}{command} user")
def op(bot, line):
	opstring = "+"
	count = 0
	for user in line.text.split():
            count += 1

    #We need one 'o' for each person we are giving ops, i.e. +ooo nick1 nick2 nick3
	for i in range(count):
            opstring += "o"
	opstring += " "
	for user in line.text.split():
            opstring += "%s " % user

	if (line.user.nick == bot.NICK) or (line.user.nick in line.conn.SERVER.ADMINS):
		line.conn.sendraw("MODE %s %s\r\n" % (line.args[0], opstring))
