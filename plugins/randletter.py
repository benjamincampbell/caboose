from bot.command import command

@command("randletter", man = "Chooses a random letter. Usage: {leader}{command} <message>")
def randletter(bot, line):
    import string
    import random
    text = random.choice(string.digits + string.ascii_uppercase)
    
    line.conn.privmsg(line.args[0], text)
