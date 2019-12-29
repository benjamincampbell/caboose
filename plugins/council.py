@command("council", man = "Chooses at random from a selection. Usage: {leader}{command} option1, option2, option3")
def council(bot, line):
    import random
    choices = line.text.split(sep = ",")
    
    # this line removes empty strings from consecutive commas
    choices = [i for i in choices if i]
    if len(choices) > 0:
        choice = random.sample(choices, 1)
        winner = "".join(choice).strip()
        line.conn.privmsg(line.args[0], "{}: {}".format(line.user.nick, winner))
