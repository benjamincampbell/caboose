@command("help", man = "Displays list of commands")
def help(nick, channel, message, handler):
    handler.privmsg(channel, "Available commands: {}".format(", ".join(key for key 
        in handler.COMMANDS if (key != "__builtins__" and handler.COMMANDS[key].visible))))