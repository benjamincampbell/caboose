@command("choose", man = "Chooses at random from a selection. Usage: &choose option 1, option 2, option 3")
def choose(nick, channel, message, handler):
    import random
    choices = message.split(sep = ",")
    #this line removes empty strings from consecutive commas
    choices = [i for i in choices if i != '']
    try:
        choice = random.sample(choices, 1)
        winner = "".join(choice).strip()
        handler.privmsg(channel, "{}: {}".format(nick, winner))
    except:
        handler.privmsg(channel, "{}: Please enter choices".format(nick))
