@command("pm", man = "Private Messages a user. No real purpose.")
def pm(nick, channel, message, handler):
    #!pm targetUser message
    try:
        targetUser = message.split()[0]
        pmessage = message.split(" ", 1)[1]
        handler.privmsg(targetUser, '{}: {}'.format(nick, pmessage))
    except:
        handler.privmsg(channel, '{}: Incorrect format, usage: pm user message')