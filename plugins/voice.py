@command("voice", man = "Gives voice to a user. Usage: &voice user")
def voice(nick, channel, message, handler):
    voicestring = "+"
    
    for user in message.split():
            voicestring += "v"
            
    voicestring += " "
    for user in message.split():
            voicestring += "%s " % user

    if (nick == handler.NICK) or (nick in handler.SETTINGS.globaladmins) :
        handler.sendraw("MODE %s %s\r\n" % (channel, voicestring))
    else:
        handler.privmsg(channel, '{}: You don\'t have permission to do that'.format(nick))
