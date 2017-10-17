import bot.command
import bot.core
import logging
import os

logging.basicConfig(filename=os.path.abspath('caboose.log'),level=logging.DEBUG)

if __name__ == "__main__":

    bot = bot.core.Bot()

    bot.run()