@command("toggle", man = "Toggles a command on or off. Admin only")
def toggle(nick, channel, message, bot):
    if nick in bot.SETTINGS.globaladmins:
        if message in bot.COMMANDS:
            #Toggling a command on or off
            if bot.COMMANDS[message].toggle_enabled():
                bot.privmsg(channel, "{} enabled!".format(message))
            else:
                bot.privmsg(channel, "{} disabled!".format(message))
        else:
            #Toggling something else
            if message == 'autoops':
                if bot.SETTINGS.channels[channel].toggle_autoops():
                    bot.privmsg(channel, "Auto-ops enabled for channel {}".format(channel))
                else:
                    bot.privmsg(channel, "Auto-ops disabled for channel {}".format(channel))
            elif message == 'autokick':
                if bot.SETTINGS.channels[channel].toggle_autokick():
                    bot.privmsg(channel, "Auto-kick enabled for channel {}".format(channel))
                else:
                    bot.privmsg(channel, "Auto-kick disabled for channel {}".format(channel))
            elif message == 'spamlimit':
                if bot.SETTINGS.channels[channel].toggle_spamlimit():
                    bot.privmsg(channel, "Spam-limit enabled for channel {}".format(channel))
                else:
                    bot.privmsg(channel, "Spam-limit disabled for channel {}".format(channel))
            elif message == 'autovoice':
                if bot.SETTINGS.channels[channel].toggle_autovoice():
                    bot.privmsg(channel, "Auto-voice enabled for channel {}".format(channel))
                else:
                    bot.privmsg(channel, "Auto-voice disabled for channel {}".format(channel))
