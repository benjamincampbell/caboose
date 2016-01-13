@command("admin", man = "Adds people to admin list. Admin only. Usage: -admin nick1 nick2")
def admin(nick, channel, message, handler):
    if nick in handler.SETTINGS.admins:
        toadmin = message.split()
        with open("admins.txt", 'a') as f:
            for nick in toadmin:
                f.write('{}\n'.format(nick))
        handler.SETTINGS.update_adminslist()
    else:
        handler.privmsg(channel, '{}: You don\'t have permission to do that'.format(nick))

@command("unadmin", man = "Removes people from admin list. Admin only. Usage: -unadmin nick1 nick2")
def unadmin(nick, channel, message, handler):
    if nick in handler.SETTINGS.admins:
        with open("admins.txt", 'r') as f:
            adminslist = f.read().splitlines()
        with open("admins.txt", 'w') as f:
            for nick in adminslist:
                if nick not in message.split():
                    f.write("{}\n".format(nick))
        handler.SETTINGS.update_adminslist()
    else:
        handler.privmsg(channel, '{}: You don\'t have permission to do that'.format(nick))

@command("join", man = "Makes Caboose join a channel. Admin only. Usage: -join #channel  (must type #)")
def join(nick, channel, message, handler):
    if nick in handler.SETTINGS.admins:
        if len(message.split()) == 1:
            handler.join(message)
    else:
        handler.privmsg(channel, '{}: You don\'t have permission to do that'.format(nick))

@command("leave", man = "Makes Caboose leave the current channel. Admin only. Usage: -leave")
def leave(nick, channel, message, handler):
    if nick in handler.SETTINGS.admins:
        handler.leave(channel)
    else:
        handler.privmsg(channel, '{}: You don\'t have permission to do that'.format(nick))

@command("quit", man = "Makes Caboose quit. Usage: -quit")
def quit(nick, channel, message, handler):
    if nick in handler.SETTINGS.admins:
        quit()
    else:
        handler.privmsg(channel, '{}: You don\'t have permission to do that'.format(nick))

@command("ignore", man = "Makes Caboose ignore one or more nicks. Admin only. Usage: -ignore nick1 nick2")
def ignore(nick, channel, message, handler):
    if nick in handler.SETTINGS.admins:
        toignore = message.split()
        with open("ignore.txt", 'a') as f:
            for nick in toignore:
                f.write('{}\n'.format(nick))
        handler.SETTINGS.update_ignorelist()
    else:
        handler.privmsg(channel, '{}: You don\'t have permission to do that'.format(nick))

@command("unignore", man = "Makes Caboose stop ignoring one or more nicks. Admin only. Usage: -unignore nick1 nick2")
def uningore(nick, channel, message, handler):
    if nick in handler.SETTINGS.admins:
        with open("ignore.txt", 'r') as f:
            ignorelist = f.read().splitlines()
            print(ignorelist)
        with open("ignore.txt", 'w') as f:
            for nick in ignorelist:
                if nick not in message.split():
                    f.write("{}\n".format(nick))
        handler.SETTINGS.update_ignorelist()
    else:
        handler.privmsg(channel, '{}: You don\'t have permission to do that'.format(nick))

@command("ignorelist", man = "Prints the list of nicks Caboose ignores. Admin only. Usage: -ignorelist")
def ignorelist(nick, channel, message, handler):
    ignoring = ""
    for nick in handler.SETTINGS.ignore:
        ignoring += "{}, ".format(nick)
    handler.privmsg(channel, "Ignoring: {}".format(ignoring))
