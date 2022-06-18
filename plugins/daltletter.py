from bot.command import command

@command("daltletter", man = "Chooses a weighted random letter for dalton. Usage: {leader}{command} <message>")
def randletter(bot, line):
    import string
    import random
    text = random.choice(string.ascii_uppercase)
    
    line.conn.privmsg(line.args[0], text)
