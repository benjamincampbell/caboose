@command("voice", man = "Gives voice to a user. Usage: &voice user")
def voice(nick, channel, message, bot):
    voicestring = "+"
    
    for user in message.split():
            voicestring += "v"
            
    voicestring += " "
    for user in message.split():
            voicestring += "%s " % user

    if (nick == bot.NICK) or (nick in bot.SETTINGS.globaladmins) :
        bot.sendraw("MODE %s %s\r\n" % (channel, voicestring))
    else:
        bot.privmsg(channel, '{}: You don\'t have permission to do that'.format(nick))
