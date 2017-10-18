@command("source", man="Displays Caboose's source. Usage: {leader}{command}")
def source(bot, line):
    line.conn.privmsg(line.args[0], "https://github.com/benjamincampbell/caboose")