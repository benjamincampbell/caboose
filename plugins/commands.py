@command("commands", man = "Displays list of commands. Usage: {leader}{command}")
def commands(bot, line):
    line.conn.privmsg(line.user.nick, "Available commands: {}".format(", ".join(key for key 
        in bot.COMMANDS if (key != "__builtins__" and bot.COMMANDS[key].visible))))
    #Add functionality to display ** after command if it's disabled (footnote after explaining so)
