def admin(nick, channel, message, privmsg):
    cmdname = message.split()
    cmd = cmdname[0]
    name = cmdname[1]

    with open("admins.txt", 'r') as r: 
        adminslist = r.read().splitlines()

    if nick in adminslist:
        if cmd == "add":
            with open("admins.txt", 'a') as r:
                r.write(name + "\n")
            privmsg(channel, '{}: {}'.format(nick, name + " added to admins"))
        elif cmd == "remove":
            if name != "twitch":
                with open("admins.txt", 'w') as r:
                    for adminline in adminslist:
                        if adminline != name:
                            r.write(adminline + "\n")
                privmsg(channel, '{}: {}'.format(nick, name + " removed from admins"))
            else:
                privmsg(channel, '{}: {}'.format(nick, "Can't let you do that, Star Fox."))
        else:
            pass
    else:
        pass

    with open("admins.txt", 'r') as r: 
        adminslist = r.read().splitlines()
    print("Admins:")
    print(adminslist)