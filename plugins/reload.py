@command("reload", man="[ADMIN ONLY] Reload commands from plugins/ folder. Use to update edited commands without reboot. Usage: {leader}{command}")
def reload(bot, line):
    import bot.command as command

    bot.COMMANDS = command.reload_commands()[0]
    command.decorate_mans(bot.LEADER, bot.COMMANDS)
