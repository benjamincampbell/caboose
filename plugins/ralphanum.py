from bot.command import command

@command("ralphanum", man = "Chooses a random number or letter. Usage: {leader}{command} <message>")
def ralphanum(bot, line):
    import string
    import random
    text = random.choice(string.digits + string.ascii_uppercase)
    
    line.conn.privmsg(line.args[0], text)
