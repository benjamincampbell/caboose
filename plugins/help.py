def help(nick, channel, message, handler):
    handler.privmsg(channel, "Available commands: {}".format(", ".join(key for key 
        in handler.COMMANDS if key != "__builtins__")))

    #TODO: This currently also displays imported modules such as datetime, random, etc.
    #Fix so it only shows commands users can access, might have to use decorators.