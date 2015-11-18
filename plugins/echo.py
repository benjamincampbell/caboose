from bot.reload import command

@command("echo", man = "Repeats back what is said. Syntax:  -echo message")
def echo(nick, channel, message, handler):
        handler.privmsg(channel, message)
