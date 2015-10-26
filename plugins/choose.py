import random

@command("choose", man = "Chooses at random from a selection. Usage: &choose option 1, option 2, option 3")
def choose(nick, channel, message, handler):
    choices = message.split(sep = ",")
    #this line removes empty strings from consecutive commas
    choices = [i for i in choices if i != '']
    choice = random.sample(choices, 1)
    #this line makes the choice string look better, no leading spaces or brackets
    winner = "".join(choice).strip()

    handler.privmsg(channel, "{}: {}".format(nick, winner))