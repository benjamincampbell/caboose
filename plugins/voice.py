@command("voice", man = "Gives voice to a user. Usage: {leader}{command} <users>")
def voice(bot, line):
    voicestring = "+"
    
    for user in line.text.split():
            voicestring += "v"
            
    voicestring += " "
    for user in line.text.split():
            voicestring += "%s " % user

    if (line.user.nick == bot.NICK) or (line.user.nick in line.conn.SERVER.ADMINS) :
        line.conn.sendraw("MODE %s %s\r\n" % (line.args[0], voicestring))
