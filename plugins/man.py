@command("man", man = "Displays information about and how to use a command. Usage: {leader}{command} <command>")
def man(bot, line):
    if line.text in bot.COMMANDS:
        line.conn.privmsg(line.args[0], bot.COMMANDS[line.text].man)
    else:
        bot.privmsg(channel, "Unknown command '{}'".format(message))