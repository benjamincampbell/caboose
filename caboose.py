import bot.settings
import bot.reload
import bot.irc
import bot.reminder_check
import os
import threading

if __name__ == "__main__":
    settings_dict = bot.settings.get_config()

    handler = bot.irc.irc_handler(settings_dict['host'], 
        settings_dict['port'], settings_dict['nick'], 
        settings_dict['startchannels'], settings_dict['leader'],
        bot.reload.reload_commands())

    #These lines start the reminder_check thread that checks every 60 seconds
    t = threading.Timer(60.0, bot.reminder_check.remindercheck, [handler.privmsg])
    t.daemon = True
    t.start()
    handler.listen()