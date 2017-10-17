@command("admin", man = "[ADMIN ONLY] Adds people to admin list. Usage: {leader}{command} nick1 nick2")
def admin(bot, line):
    import yaml
    if line.user.nick in line.conn.SERVER.ADMINS:
        if len(line.text.split()) == 1:
            bot.CFG['servers'][line.conn.SERVER.NAME]['admins'].append(line.text.strip())
            bot.update_config()

@command("unadmin", man = "[ADMIN ONLY] Removes people from admin list. Usage: {leader}{command} nick1 nick2")
def unadmin(bot, line):
    if line.user.nick in line.conn.SERVER.ADMINS:
        if len(line.text.split()) == 1:
            bot.CFG['servers'][line.conn.SERVER.NAME]['admins'].remove(line.text.strip())
            bot.update_config()

@command("join", man = "[ADMIN ONLY] Makes Caboose join a channel. Usage: {leader}{command} #channel  (must type #)")
def join(bot, line):
    from bot.connection import Channel
    if line.user.nick in line.conn.SERVER.ADMINS:
        if len(line.text.split()) == 1:
            line.conn.join(line.text)
            line.conn.SERVER.CHANNELS[line.text] = Channel(line.text)
            #I think I also need to have him make a channel options object for the new channel here

@command("leave", man = "[ADMIN ONLY] Makes Caboose leave the current channel. Usage: {leader}{command}")
def leave(bot, line):
    if line.user.nick in line.conn.SERVER.ADMINS:
        if line.text == '':
            line.conn.leave(line.args[0])

@command("quit", man = "[ADMIN ONLY] Makes Caboose quit. Usage: {leader}{command}")
def quit(bot, line):
    if line.user.nick in line.conn.SERVER.ADMINS:
        quit()

@command("ignore", man = "[ADMIN ONLY] Makes Caboose ignore one or more nicks. Usage: {leader}{command} nick1 nick2")
def ignore(bot, line):
    if line.user.nick in line.conn.SERVER.ADMINS:
        if len(line.text.split()) == 1:
            bot.CFG['servers'][line.conn.SERVER.NAME]['ignore'].append(line.text.strip())
            bot.update_config()

@command("unignore", man = "[ADMIN ONLY] Makes Caboose stop ignoring one or more nicks. Usage: {leader}{command} nick1 nick2")
def uningore(bot, line):
    if line.user.nick in line.conn.SERVER.ADMINS:
        if len(line.text.split()) == 1:
            bot.CFG['servers'][line.conn.SERVER.NAME]['ignore'].remove(line.text.strip())
            bot.update_config()

@command("ignorelist", man = "[ADMIN ONLY] Prints the list of nicks Caboose ignores. Usage: {leader}{command}")
def ignorelist(bot, line):
    ignoring = ' '.join(n for n in bot.CFG['servers'][line.conn.SERVER.NAME]['ignore'])
    line.conn.privmsg(line.args[0], "Ignoring: {}".format(ignoring))
    
@command("kick", man = "[ADMIN ONLY] Kicks a user with a message. Usage: {leader}{command} <user> <message>")
def kick(bot, line):
    if (line.user.nick in line.conn.SERVER.ADMINS):
        if (len(line.text.split()) == 1):
            u = line.text.strip()
            m = ''
            line.conn.kick(line.args[0], u, m)
        elif (len(line.text.split()) > 1):
            u, m = line.text.split(' ', 1)
            line.conn.kick(line.args[0], u, m)
            