@command("admin", man = "[ADMIN ONLY] Adds people to admin list. Usage: &admin nick1 nick2")
def admin(nick, channel, message, bot):
    if nick in bot.SETTINGS.globaladmins:
        toadmin = message.split()
        with open("globaladmins.txt", 'a') as f:
            for nick in toadmin:
                f.write('{}\n'.format(nick))
        bot.SETTINGS.update_adminlist()
    else:
        bot.privmsg(channel, '{}: You don\'t have permission to do that'.format(nick))

@command("unadmin", man = "[ADMIN ONLY] Removes people from admin list. Usage: &unadmin nick1 nick2")
def unadmin(nick, channel, message, bot):
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

@command("join", man = "[ADMIN ONLY] Makes Caboose join a channel. Usage: &join #channel  (must type #)")
def join(nick, channel, message, bot):
    from bot.settings import ChannelOptions

    if nick in bot.SETTINGS.globaladmins:
        if len(message.split()) == 1:
            bot.join(message)
            bot.CHANNELS[message] = ChannelOptions()
            #I think I also need to have him make a channel options object for the new channel here
    else:
        bot.privmsg(channel, '{}: You don\'t have permission to do that'.format(nick))

@command("leave", man = "[ADMIN ONLY] Makes Caboose leave the current channel. Usage: &leave")
def leave(nick, channel, message, bot):
    if nick in bot.SETTINGS.globaladmins:
        bot.leave(channel)
    else:
        bot.privmsg(channel, '{}: You don\'t have permission to do that'.format(nick))

@command("quit", man = "[ADMIN ONLY] Makes Caboose quit. Usage: &quit")
def quit(nick, channel, message, bot):
    if nick in bot.SETTINGS.globaladmins:
        quit()
    else:
        bot.privmsg(channel, '{}: You don\'t have permission to do that'.format(nick))

@command("ignore", man = "[ADMIN ONLY] Makes Caboose ignore one or more nicks. Usage: &ignore nick1 nick2")
def ignore(nick, channel, message, bot):
    if nick in bot.SETTINGS.globaladmins:
        toignore = message.split()
        with open("ignore.txt", 'a') as f:
            for nick in toignore:
                f.write('{}\n'.format(nick))
        bot.SETTINGS.update_ignorelist()
    else:
        bot.privmsg(channel, '{}: You don\'t have permission to do that'.format(nick))

@command("unignore", man = "[ADMIN ONLY] Makes Caboose stop ignoring one or more nicks. Usage: &unignore nick1 nick2")
def uningore(nick, channel, message, bot):
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

@command("ignorelist", man = "[ADMIN ONLY] Prints the list of nicks Caboose ignores. Usage: &ignorelist")
def ignorelist(nick, channel, message, bot):
    ignoring = ""
    for nick in bot.SETTINGS.ignore:
        ignoring += "{}, ".format(nick)
    bot.privmsg(channel, "Ignoring: {}".format(ignoring))
    
@command("kick", man = "[ADMIN ONLY] Kicks a user with a message. Usage: &kick <user> <message>")
def kick(nick, channel, message, bot):

    if (nick == bot.NICK) or (nick in bot.SETTINGS.globaladmins):
        if message.split()[0] == "set":
            bot.SETTINGS.channels[channel].autokick_message = message.split()[1:]
        else:
            bot.kick(channel, nick, message)
    else:
        bot.privmsg(channel, '{}: You don\'t have permission to do that'.format(nick))
