@command("epstein", man = "States the obvious")
def echo(bot, line): 
    line.conn.privmsg(line.args[0], "did not kill himself")
