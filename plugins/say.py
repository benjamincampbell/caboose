from bot.command import command

@command("say", man = "Says a message to the given channel. Usage: {leader}{command} <#channel> <message>")
def echo(bot, line):

    linesplit = line.text.split()

    channel = linesplit[0]
    message = ' '.join(linesplit[1:])

    if (channel[0] != '#'):
        line.conn.privmsg(line.args[0], "channels start with a # you dingus")
    else:
        line.conn.privmsg(channel, message)

