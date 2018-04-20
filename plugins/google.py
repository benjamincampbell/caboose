from bot.command import command

@command("google", aliases = ["g"], man = "Perform a google search, returning the first result. Usage: {leader}{command} <query>")
def google(bot, line):
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
                num=1
            ).execute()

            res = search_res["items"][0]
            title = res["title"]
            link = res["link"]

            short_url = shorten_url(bot, link)

            text = "{0} - {1}".format(
                short_url,
                title)

            line.conn.privmsg(line.args[0], text)
        except Exception as e:
            line.conn.privmsg(line.args[0], "Error: {0}".format(e))

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
        except Exception as e:
            line.conn.privmsg(line.args[0], "Error: {0}".format(e))
