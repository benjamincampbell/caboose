import bot.command
import bot.core
import logging
import os
import sys

if sys.argv[1] == "DEBUG":
    logging.basicConfig(filename=os.path.abspath('caboose.log'),level=logging.DEBUG)
elif sys.argv[1] == "INFO":
    logging.basicConfig(filename=os.path.abspath('caboose.log'),level=logging.INFO)
elif sys.argv[1] == "WARNING":
    logging.basicConfig(filename=os.path.abspath('caboose.log'),level=logging.WARNING)
elif sys.argv[1] == "ERROR":
    logging.basicConfig(filename=os.path.abspath('caboose.log'),level=logging.ERROR)
else:
    logging.basicConfig(filename=os.path.abspath('caboose.log'),level=logging.INFO)

if __name__ == "__main__":

    bot = bot.core.Bot()

    bot.run()
