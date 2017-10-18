@command("echo", man = "Repeats back what is said. Usage: {leader}{command} <message>")
def echo(bot, line):
        from .colors import color
        line.conn.privmsg(color(line.args[0], 'red', 'green'), line.text)
