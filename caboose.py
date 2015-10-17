import bot.settings
import bot.reload
import bot.irc
import bot.reminder_check
import os

if __name__ == "__main__":
    settings_dict = bot.settings.get_config()

    handler = bot.irc.irc_handler(settings_dict['host'], 
        settings_dict['port'], settings_dict['nick'], 
        settings_dict['startchannels'], settings_dict['leader'],
        bot.reload.reload_commands())
    bot.reminder_check.remindercheck(handler.privmsg)
    handler.listen()