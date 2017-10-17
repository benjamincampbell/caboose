@command("toggle", man = "[ADMIN ONLY] Toggles a command on or off. Usage: {leader}{command} <option or command>")
def toggle(bot, line):
    if line.user.nick in line.conn.SERVER.ADMINS:
        if line.text in bot.COMMANDS:
            #Toggling a command on or off
            if bot.COMMANDS[line.text].toggle_enabled():
                line.conn.privmsg(line.args[0], "{} enabled!".format(line.text))
            else:
                line.conn.privmsg(line.args[0], "{} disabled!".format(line.text))
        else:
            #Toggling something else
            if line.text == 'autoops':
                if line.conn.SERVER.CHANNELS[line.args[0]].toggle_autoops():
                    line.conn.privmsg(line.args[0], "Auto-ops enabled for channel {}".format(line.args[0]))
                else:
                    line.conn.privmsg(line.args[0], "Auto-ops disabled for channel {}".format(line.args[0]))
            elif line.text == 'autokick':
                if line.conn.SERVER.CHANNELS[line.args[0]].toggle_autokick():
                    line.conn.privmsg(line.args[0], "Auto-kick enabled for channel {}".format(line.args[0]))
                else:
                    line.conn.privmsg(line.args[0], "Auto-kick disabled for channel {}".format(line.args[0]))
            elif line.text == 'spamlimit':
                if line.conn.SERVER.CHANNELS[line.args[0]].toggle_spamlimit():
                    line.conn.privmsg(line.args[0], "Spam-limit enabled for channel {}".format(line.args[0]))
                else:
                    line.conn.privmsg(line.args[0], "Spam-limit disabled for channel {}".format(line.args[0]))
            elif line.text == 'autovoice':
                if line.conn.SERVER.CHANNELS[line.args[0]].toggle_autovoice():
                    line.conn.privmsg(line.args[0], "Auto-voice enabled for channel {}".format(line.args[0]))
                else:
                    line.conn.privmsg(line.args[0], "Auto-voice disabled for channel {}".format(line.args[0]))
