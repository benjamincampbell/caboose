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
                if handler.SETTINGS.channels[channel].toggle_autoops():
                    handler.privmsg(channel, "Auto-ops enabled for channel {}".format(channel))
                else:
                    handler.privmsg(channel, "Auto-ops disabled for channel {}".format(channel))
            elif message == 'spamlimit':
                if handler.SETTINGS.channels[channel].toggle_spamlimit():
                    handler.privmsg(channel, "Spam-limit enabled for channel {}".format(channel))
                else:
                    handler.privmsg(channel, "Spam-limit disabled for channel {}".format(channel))
            elif message == 'autovoice':
                if handler.SETTINGS.channels[channel].toggle_autovoice():
                    handler.privmsg(channel, "Auto-voice enabled for channel {}".format(channel))
                else:
                    handler.privmsg(channel, "Auto-voice disabled for channel {}".format(channel))
