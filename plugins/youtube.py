@command("youtube", aliases = ["yt"], man = "Perform a YouTube search, returning the first result. Usage: {leader}{command} <query>")
def image(bot, line):

    query = line.text
    if query == "":
        line.conn.privmsg(line.args[0], "Please enter a search query")
    else:
        cse_id = bot.SECRETS["other"]["google_cse_id"]

        try:
            search_res = bot.google_search_service.cse().list(
                q=query,
                cx=cse_id,
                siteSearch="youtube.com",
                num=1
            ).execute()

            res = search_res["items"][0]
            link = res["link"]
            title = res["title"]

            shorturl_res = bot.google_urlshortener_service.url().insert(
                body={
                    'longUrl': link
                }
            ).execute()

            short_url = shorturl_res["id"]

            text = "{0} - {1}".format(
                short_url,
                title
                )

            line.conn.privmsg(line.args[0], text)
        except:
            line.conn.privmsg(line.args[0], "Error during search")
