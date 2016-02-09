@command("toggle", man = "Toggles a command on or off. Admin only")
def toggle(nick, channel, message, handler):
	if (message in handler.COMMANDS and nick in handler.SETTINGS.globaladmins):
		if handler.COMMANDS[message].toggle_enabled():
			handler.privmsg(channel, "{} enabled!".format(message))
		else:
			handler.privmsg(channel, "{} disabled!".format(message))