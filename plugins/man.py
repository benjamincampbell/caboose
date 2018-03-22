@command("man", aliases = ["help"], man = "Displays information about and how to use a command. Usage: {leader}{command} <command>")
def man(bot, line):
    if line.text in bot.COMMANDS:
        line.conn.privmsg(line.user.nick, bot.COMMANDS[line.text].man)
    else:
        line.conn.privmsg(line.user.nick, "Unknown command {0}".format(line.text))
