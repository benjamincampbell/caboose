@command("pm", man = "Private Messages a user. No real purpose.")
def pm(nick, channel, message, bot):
    #!pm targetUser message
    try:
        targetUser = message.split()[0]
        pmessage = message.split(" ", 1)[1]
        bot.privmsg(targetUser, '{}: {}'.format(nick, pmessage))
    except:
        bot.privmsg(channel, '{}: Incorrect format, usage: pm user message')