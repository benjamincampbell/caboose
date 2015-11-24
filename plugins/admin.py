@command("admin", man = "Adds or removes people from admin list. Admin only. Usage: -admin add/remove name")
def admin(nick, channel, message, handler):
    try:
        cmd, name = message.split()

        if nick in handler.SETTINGS.admins:
            if cmd == "add":
                with open("admins.txt", 'a') as r:
                    r.write("name\n".format(name))
                handler.privmsg(channel, '{}: {}'.format(nick, name + " added to admins"))
            elif cmd == "remove":
                if name != "twitch":
                    with open("admins.txt", 'w') as r:
                        for adminline in adminslist:
                            if adminline != name:
                                r.write(adminline + "\n")
                    handler.privmsg(channel, '{}: {}'.format(nick, name + " removed from admins"))
                else:
                    handler.privmsg(channel, '{}: {}'.format(nick, "Can't let you do that, Star Fox."))
            else:
                pass
        else:
            pass
    
        with open("admins.txt", 'r') as r: 
            adminslist = r.read().splitlines()
        print("Admins:")
        print(adminslist)
    except ValueError:
        handler.privmsg(channel, '{}: One at a time, please, I\'m not a barbarian'.format(nick))

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
        toignore = []
        for nick in message.split():
            toignore.append(nick)
        with open("ignore.txt", 'a') as f:
            for nick in toignore:
                f.write('{}\n'.format(nick))
        handler.SETTINGS.update()
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
        handler.SETTINGS.update()
    else:
        handler.privmsg(channel, '{}: You don\'t have permission to do that'.format(nick))

@command("ignorelist", man = "Prints the list of nicks Caboose ignores. Admin only. Usage: -ignorelist")
def ignorelist(nick, channel, message, handler):
    ignoring = ""
    for nick in handler.SETTINGS.ignore:
        ignoring += "{}, ".format(nick)
    handler.privmsg(channel, "Ignoring: {}".format(ignoring))