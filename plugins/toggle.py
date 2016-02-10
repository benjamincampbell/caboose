@command("toggle", man = "Toggles a command on or off. Admin only")
def toggle(nick, channel, message, handler):
    if nick in handler.SETTINGS.globaladmins:
        if message in handler.COMMANDS:
            #Toggling a command on or off
            if handler.COMMANDS[message].toggle_enabled():
                handler.privmsg(channel, "{} enabled!".format(message))
            else:
                handler.privmsg(channel, "{} disabled!".format(message))
        else:
            #Toggling something else
            if message == 'autoops':
                handler.SETTINGS.channels[channel].toggle_autoops()
            elif message == 'spamlimit':
                handler.SETTINGS.channels[channel].toggle_spamlimit()