

@command("youtube", aliases = ["yt"], man = "Perform a YouTube search, returning the first result. Usage: {leader}{command} <query>")
def youtube(bot, line):

    def get_playtime(raw_playtime):
        playtime = raw_playtime[2:]
        playtime_min_split = playtime.split('M')
        raw_mins = playtime_min_split[0]
        hours = int(raw_mins) // 60
        mins = int(raw_mins) % 60
        raw_secs = playtime_min_split[1]
        secs = int(raw_secs.split('S')[0])

        if hours == 0:
            return "{0:02d}:{1:02d}".format(mins, secs)
        else:
            return "{0:02d}:{1:02d}:{2:02d}".format(int(hours), mins, secs)

    query = line.text
    if query == "":
        line.conn.privmsg(line.args[0], "Please enter a search query")
    else:
        cse_id = bot.SECRETS["other"]["google_cse_id"]

        # try:
        search_res = bot.google_search_service.cse().list(
            q=query,
            cx=cse_id,
            siteSearch="youtube.com",
            num=1
        ).execute()

        res = search_res["items"][0]

        link = res["link"]
        title = res["title"]
        views = res["pagemap"]["videoobject"][0]["interactioncount"]
        raw_playtime = res["pagemap"]["videoobject"][0]["duration"]
        playtime = get_playtime(raw_playtime)

        shorturl_res = bot.google_urlshortener_service.url().insert(
            body={
                'longUrl': link
            }
        ).execute()

        short_url = shorturl_res["id"]

        text = "{0} - {1} [{2}] [{3} views]".format(
            short_url,
            title,
            playtime,
            views)

        line.conn.privmsg(line.args[0], text)
        # except:
        #     line.conn.privmsg(line.args[0], "Error during search")
