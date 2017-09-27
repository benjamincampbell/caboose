@command("man", man = "Displays information about and how to use a command. Usage: &man command")
def man(nick, channel, message, bot):
    if message in bot.COMMANDS:
        bot.privmsg(channel, bot.COMMANDS[message].man)
    else:
        bot.privmsg(channel, "unknown command '{}'".format(message))