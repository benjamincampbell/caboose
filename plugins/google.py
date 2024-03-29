from bot.command import command

@command("google", aliases = ["g"], man = "Perform a google search, returning the first result. Usage: {leader}{command} <query>")
def google(bot, line):
    from plugins.shorten import shorten_url
    import random

    query = line.text
    if query == "":
        line.conn.privmsg(line.args[0], "Please enter a search query")
    else:
        cse_id = bot.SECRETS["other"]["google_cse_id"]

        try:
            search_res = bot.google_search_service.cse().list(
                q=query,
                cx=cse_id,
                num=1
            ).execute()

            res = search_res["items"][0]
            title = res["title"]
            link = res["link"]
            displaylink = res["displayLink"]
            print(res)

            short_url = shorten_url(bot, link)

            text = "{0} - {1} - {2}".format(
                short_url,
                displaylink,
                title)

            line.conn.privmsg(line.args[0], text)
        except KeyError as e:
            logger = logging.getLogger("log")
            logger.warning("Error: {0}".format(e))
            line.conn.privmsg(line.args[0], "No results found.")
        except Exception as e:
            logger = logging.getLogger("log")
            logger.warning("Error: {0}".format(e))
            line.conn.privmsg(line.args[0], "Error: Check logs")

@command("image", aliases = ["gis"], man = "Perform a google image search, returning the first result. Usage: {leader}{command} <query>")
def image(bot, line):
    from plugins.shorten import shorten_url

    query = line.text
    if query == "":
        line.conn.privmsg(line.args[0], "Please enter a search query")
    else:
        cse_id = bot.SECRETS["other"]["google_cse_id"]

        try:
            search_res = bot.google_search_service.cse().list(
                q=query,
                cx=cse_id,
                searchType="image",
            ).execute()

            res = search_res["items"][0]
            link = res["link"]

            short_url = shorten_url(bot, link)

            text = "{0}".format(
                short_url,
                )

            line.conn.privmsg(line.args[0], text)
        except KeyError as e:
            logger = logging.getLogger("log")
            logger.warning("Error: {0}".format(e))
            line.conn.privmsg(line.args[0], "No results found.")
        except Exception as e:
            logger = logging.getLogger("log")
            logger.warning("Error: {0}".format(e))
            line.conn.privmsg(line.args[0], "Error, check logs")


@command("gif", aliases = [], man = "Perform a google image search, returning the the first gif. Usage: {leader}{command} <query>")
def image(bot, line):
    from plugins.shorten import shorten_url

    query = line.text
    if query == "":
        line.conn.privmsg(line.args[0], "Please enter a search query")
    else:
        cse_id = bot.SECRETS["other"]["google_cse_id"]

        try:
            search_res = bot.google_search_service.cse().list(
                q=query + " filetype:gif",
                cx=cse_id,
                searchType="image",
            ).execute()

            res = search_res["items"][0]
            link = res["link"]

            short_url = shorten_url(bot, link)

            text = "{0}".format(
                short_url,
                )

            line.conn.privmsg(line.args[0], text)
        except KeyError as e:
            logger = logging.getLogger("log")
            logger.warning("Error: {0}".format(e))
            line.conn.privmsg(line.args[0], "No results found.")
        except Exception as e:
            logger = logging.getLogger("log")
            logger.warning("Error: {0}".format(e))
            line.conn.privmsg(line.args[0], "Error, check logs")
