import pprint

def help(nick, channel, message, handler):

    #iterate through the handler.COMMANDS dictionary's keys, take all except __builtins__.
    #that should give all the user commands


    handler.privmsg(channel, "Available commands: {}".format())
