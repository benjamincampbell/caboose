@command("admin", man = "[ADMIN ONLY] Adds people to admin list. Usage: {leader}{command} nick1 nick2")
def admin(bot, line):
    if line.user.nick in line.conn.SERVER.ADMINS:
        if line.text.split() == 1:
            
    else:
        bot.privmsg(channel, '{}: You don\'t have permission to do that'.format(nick))

@command("unadmin", man = "[ADMIN ONLY] Removes people from admin list. Usage: {leader}{command} nick1 nick2")
def unadmin(bot, line):
    if nick in bot.SETTINGS.globaladmins:
        with open("globaladmins.txt", 'r') as f:
            adminlist = f.read().splitlines()
        with open("globaladmins.txt", 'w') as f:
            for nick in adminlist:
                if nick not in message.split():
                    f.write("{}\n".format(nick))
        bot.SETTINGS.update_adminlist()
    else:
        bot.privmsg(channel, '{}: You don\'t have permission to do that'.format(nick))

@command("join", man = "[ADMIN ONLY] Makes Caboose join a channel. Usage: {leader}{command} #channel  (must type #)")
def join(bot, line):
    from bot.connection import Channel
    if line.user.nick in line.conn.SERVER.ADMINS:
        if len(line.text.split()) == 1:
            line.conn.join(line.text)
            line.conn.SERVER.CHANNELS[line.text] = Channel(line.text)
            #I think I also need to have him make a channel options object for the new channel here
    else:
        line.conn.privmsg(channel, '{}: You don\'t have permission to do that'.format(nick))

@command("leave", man = "[ADMIN ONLY] Makes Caboose leave the current channel. Usage: {leader}{command}")
def leave(line):
    if nick in bot.SETTINGS.globaladmins:
        bot.leave(channel)
    else:
        bot.privmsg(channel, '{}: You don\'t have permission to do that'.format(nick))

@command("quit", man = "[ADMIN ONLY] Makes Caboose quit. Usage: {leader}{command}")
def quit(line):
    if nick in bot.SETTINGS.globaladmins:
        quit()
    else:
        bot.privmsg(channel, '{}: You don\'t have permission to do that'.format(nick))

@command("ignore", man = "[ADMIN ONLY] Makes Caboose ignore one or more nicks. Usage: {leader}{command} nick1 nick2")
def ignore(line):
    if nick in bot.SETTINGS.globaladmins:
        toignore = message.split()
        with open("ignore.txt", 'a') as f:
            for nick in toignore:
                f.write('{}\n'.format(nick))
        bot.SETTINGS.update_ignorelist()
    else:
        bot.privmsg(channel, '{}: You don\'t have permission to do that'.format(nick))

@command("unignore", man = "[ADMIN ONLY] Makes Caboose stop ignoring one or more nicks. Usage: {leader}{command} nick1 nick2")
def uningore(line):
    if nick in bot.SETTINGS.globaladmins:
        with open("ignore.txt", 'r') as f:
            ignorelist = f.read().splitlines()
            print(ignorelist)
        with open("ignore.txt", 'w') as f:
            for nick in ignorelist:
                if nick not in message.split():
                    f.write("{}\n".format(nick))
        bot.SETTINGS.update_ignorelist()
    else:
        bot.privmsg(channel, '{}: You don\'t have permission to do that'.format(nick))

@command("ignorelist", man = "[ADMIN ONLY] Prints the list of nicks Caboose ignores. Usage: {leader}{command}")
def ignorelist(line):
    ignoring = ""
    for nick in bot.SETTINGS.ignore:
        ignoring += "{}, ".format(nick)
    bot.privmsg(channel, "Ignoring: {}".format(ignoring))
    
@command("kick", man = "[ADMIN ONLY] Kicks a user with a message. Usage: {leader}{command} <user> <message>")
def kick(line):

    if (nick == bot.NICK) or (nick in bot.SETTINGS.globaladmins):
        if message.split()[0] == "set":
            bot.SETTINGS.channels[channel].autokick_message = message.split()[1:]
        else:
            bot.kick(channel, nick, message)
    else:
        bot.privmsg(channel, '{}: You don\'t have permission to do that'.format(nick))
