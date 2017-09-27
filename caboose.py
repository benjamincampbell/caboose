import bot.settings
import bot.reload
import bot.bot
import bot.reminder_check
import logging
import os

logging.basicConfig(filename=os.path.abspath('caboose.log'),level=logging.DEBUG)

if __name__ == "__main__":

    bot = bot.core.caboose_bot()

    bot.listen()