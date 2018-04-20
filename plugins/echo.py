from bot.command import command

@command("echo", man = "Repeats back what is said. Usage: {leader}{command} <message>")
def echo(bot, line):
    from bot.colors import color

    line.conn.privmsg(line.args[0], line.text)
