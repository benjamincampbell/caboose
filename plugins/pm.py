@command("pm", man = "Private Messages a user. Usage: {leader}{command} <user> <message>")
def pm(bot, line):
    if (len(line.text.split()) > 1):
        user, message = line.text.split(' ', 1)
        line.conn.privmsg(user, message)