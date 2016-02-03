@command("man", man = "Displays information about and how to use a command. Usage: &man command")
def man(nick, channel, message, handler):
    if message in handler.COMMANDS:
        handler.privmsg(channel, handler.COMMANDS[message].man)
    else:
        handler.privmsg(channel, "unknown command '{}'".format(message))