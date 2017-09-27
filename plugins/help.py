@command("help", man = "Displays list of commands")
def help(nick, channel, message, bot):
    bot.privmsg(channel, "Available commands: {}".format(", ".join(key for key 
        in bot.COMMANDS if (key != "__builtins__" and bot.COMMANDS[key].visible))))
    #Add functionality to display ** after command if it's disabled (footnote after explaining so)