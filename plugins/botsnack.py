@command("botsnack", man = "Bots can have a little snack, as a treat")
def echo(bot, line): 
    line.conn.privmsg(line.args[0], "they're a little rough on you meatbags")
