from bot.command import command

@command("reload", man="[ADMIN ONLY] Reload commands from plugins/ folder. Use to update edited commands without reboot. Usage: {leader}{command}")
def reload(bot, line):
    import bot.command as command
    import bot.response as response

    bot.COMMANDS = command.reload_commands()[0] # 0 index is commands, 1 is tables
    bot.RESPONSES = response.reload_responses()
    command.decorate_mans(bot.LEADER, bot.COMMANDS)
