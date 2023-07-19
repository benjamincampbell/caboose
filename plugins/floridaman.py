from bot.command import command

@command("floridaman", aliases = ["florida"], man = "Returns a random Florida Man article from a google search. Usage: {leader}{command}")
def floridaman(bot, line):
    import random
    import logging
    from plugins.google import google
    from plugins.shorten import shorten_url

    all_results = []
    start_result = 1

    try:
        while (start_result < 100):
            cse_id = bot.SECRETS["other"]["google_cse_id"]
            search_res = bot.google_search_service.cse().list(
                q="florida man news",
                cx=cse_id,
                start=start_result
            ).execute()

            start_result += 10

            res = search_res["items"]
            florida_results = list(filter(lambda x: "florida man" in x["title"].lower(), res))
            all_results.extend(florida_results)


        winner = random.choice(florida_results)

        title = winner["title"]
        link = winner["link"]

        short_url = shorten_url(bot, link)

        text = "{0} - {1}".format(
            short_url,
            title)

        line.conn.privmsg(line.args[0], text)
    except Exception as e:
        logger = logging.getLogger("log")
        logger.warning("Error: {0}".format(e))