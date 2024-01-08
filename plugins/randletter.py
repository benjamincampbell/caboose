from bot.command import command

@command("randletter", man = "Chooses a random letter. Optionally supply number to return multiple letters.  Usage: {leader}{command} <number> ")
def randletter(bot, line):
    import string
    import random

    linesplit = line.text.split()
    if len(linesplit) > 1:
        # too many arguments
        line.conn.privmsg(line.user.nick, "Too many arguments supplied")
        return None
    elif len(linesplit) == 0:
    # always return one item if the user did not supply a number of items to return    
        num = 1
        text = random.sample(string.ascii_uppercase, num)
    elif len(linesplit) == 1:
        if linesplit[0].isdigit() and int(linesplit[0]) < 6:
            if int(linesplit[0]) == 0:
                num = 1
            else: 
                num = int(linesplit[0])

            text = random.sample(string.ascii_uppercase, num)
        else: 
            line.conn.privmsg(line.user.nick, "Please enter a number between 1 and 5.")
            return None
    else:
        line.conn.privmsg(line.user.nick, "Please enter a number between 1 and 5.")

    line.conn.privmsg(line.args[0], text)
