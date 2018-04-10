from bot.command import command

@command("google", aliases = ["g"], man = "Perform a google search, returning the first result. Usage: {leader}{command} <query>")
def google(bot, line):
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
            display_link = res["displayLink"]

            shorturl_res = bot.google_urlshortener_service.url().insert(
                body={
                    'longUrl': res["formattedUrl"]
                }
            ).execute()

            short_url = shorturl_res["id"]

            text = "{0} - {1} - {2}".format(
                short_url,
                display_link,
                title)

            line.conn.privmsg(line.args[0], text)
        except:
            line.conn.privmsg(line.args[0], "Error during search")
