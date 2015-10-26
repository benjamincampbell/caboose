@command("admin", man = "Adds or removes people from admin list. Usage: &admin add/remove name")
def admin(nick, channel, message, handler):
    try:
        cmd, name = message.split()

        with open("admins.txt", 'r') as r: 
            adminslist = r.read().splitlines()

        if nick in adminslist:
            if cmd == "add":
                with open("admins.txt", 'a') as r:
                    r.write(name + "\n")
                handler.privmsg(channel, '{}: {}'.format(nick, name + " added to admins"))
            elif cmd == "remove":
                if name != "twitch":
                    with open("admins.txt", 'w') as r:
                        for adminline in adminslist:
                            if adminline != name:
                                r.write(adminline + "\n"
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

@command("join", man = "Makes Caboose join a channel. Admin only. Usage: &join #channel  (must type #)")
def join(nick, channel, message, handler):
    with open("admins.txt", 'r') as r:
        if nick in r.read().splitlines():
            if len(message.split()) == 1:
                handler.join(message)
        else:
            handler.privmsg(channel, '{}: You don\'t have permission to do that'.format(nick))

@command("leave", man = "Makes Caboose leave the current channel. Admin only. Usage: &leave")
def leave(nick, channel, message, handler):
    with open("admins.txt", 'r') as r:
        if nick in r.read().splitlines():
            handler.leave(channel)
        else:
            handler.privmsg(channel, '{}: You don\'t have permission to do that'.format(nick))