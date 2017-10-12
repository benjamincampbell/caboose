from bot.reload import command

@command("echo", man = "Repeats back what is said. Syntax:  &echo message")
def echo(line):
        line.conn.privmsg(line.args[0], line.text)
