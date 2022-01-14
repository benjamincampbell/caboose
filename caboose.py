import bot.command
import bot.core
import logging
import os
import sys

from logging.handlers import TimedRotatingFileHandler

if not os.path.exists("logs"):
    os.makedirs("logs")

log_name = "logs/caboose.log"
logger = logging.getLogger("log")

if len(sys.argv) > 1:
    if sys.argv[1] == "DEBUG":
        logger.setLevel(logging.DEBUG)
    elif sys.argv[1] == "INFO":
        logger.setLevel(logging.INFO)
    elif sys.argv[1] == "WARNING":
        logger.setLevel(logging.WARNING)
    elif sys.argv[1] == "ERROR":
        logger.setLevel(logging.ERROR)
else:
    logger.setLevel(logging.INFO)

handler = TimedRotatingFileHandler(log_name, when="midnight", interval=1, encoding='utf8')
handler.suffix = "%Y-%m-%d"
logger.addHandler(handler)

logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

if __name__ == "__main__":

    bot = bot.core.Bot()

    bot.run()
