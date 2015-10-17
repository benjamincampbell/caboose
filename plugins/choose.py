import random

def choose(nick, channel, message, privmsg):
    choices = message.split(sep = ",")
    #this line removes empty strings from consecutive commas
    choices = [i for i in choices if i != '']
    choice = random.sample(choices, 1)
    #this line makes the choice string look better, no leading spaces or brackets
    winner = "".join(choice).strip()

    privmsg(channel, "{}: {}".format(nick, winner))