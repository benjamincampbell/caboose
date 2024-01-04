from bot.command import command

@command("randletter", man = "Chooses a random letter. Optionally supply number to return multiple letters. Usage: {leader}{command} <number>")
def randletter(bot, line):
    import string
    import random

    linesplit = line.text.split()
    if len(linesplit) > 1:
        # too many arguments
        line.conn.privmsg(line.user.nick, "Too many arguments supplied")
        return None
    elif len(linesplit) == 1:
        if linesplit[0].isdigit() and int(linesplit[0]) < 6:
            num = int(linesplit[0])
        else:
            line.conn.privmsg(line.user.nick, "Please enter a number 5 or fewer.")

    # else no args

    text = random.sample(string.ascii_uppercase, num)

line.conn.privmsg(line.args[0], text)
