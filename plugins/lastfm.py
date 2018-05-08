from bot.command import command

@command("lastfm", aliases = ["nowplaying", "lfm", "np"], man = "Obtain most recent played song for a Last.FM user Usage: {leader}{command} <username>")
def lastfm(bot, line):
    import json
    import requests
    from datetime import datetime
    from bot.colors import color

    # testing
    import pprint

    RECENT_TRACK_URL = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={user}&api_key={api_key}&format=json"
    TRACK_INFO_URL = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={api_key}&artist={artist}&track={track}&username={user}&format=json"
    API_KEY = bot.SECRETS["api_keys"]["lastfm"]

    parts = line.text.split(' ')

    username = parts[0]

    recent_response = requests.get(RECENT_TRACK_URL.format(user=username, api_key=API_KEY))
    recent_json = json.loads(recent_response.text)

    try:
        error = recent_json["error"]
        user_exists = False
    except KeyError:
        user_exists = True

    if user_exists:
        last_fm_track_user = recent_json["recenttracks"]["@attr"]["user"]

        try:
            lastfm_track_info = recent_json["recenttracks"]["track"][0]
            track_exists = True
        except IndexError:
            track_exists = False

        if track_exists:
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(lastfm_track_info)

            lastfm_track_song = lastfm_track_info["name"]
            lastfm_track_artist = lastfm_track_info["artist"]["#text"]
            lastfm_track_album = lastfm_track_info["album"]["#text"]

            try:
                lastfm_track_time = lastfm_track_info["@attr"]["nowplaying"]
                now_playing = True
            except KeyError:
                lastfm_track_time = lastfm_track_info["date"]["#text"]
                now_playing = False

            info_response = requests.get(TRACK_INFO_URL.format(api_key=API_KEY, artist=lastfm_track_artist,
                track=lastfm_track_song, user=last_fm_track_user))
            info_json = json.loads(info_response.text)

            last_fm_track_tags = []

            try:
                lastfm_track_playcount = info_json["track"]["userplaycount"]
                track_info_exists = True
                last_fm_track_tags = info_json["track"]["toptags"]["tag"]
            except KeyError:
                track_info_exists = False
                lastfm_track_playcount = "0"

            # pp.pprint(info_json)

            if (last_fm_track_tags == []):
                tags = ""
            else:
                tags = "({0}) ".format(", ".join(t["name"] for t in last_fm_track_tags))

            if now_playing:
                msg = "{0} is listening to {1} by {2} from the album {3} {4}[playcount: {5}]".format(color(last_fm_track_user, 'green'),
                    color(lastfm_track_song, 'lightblue'), color(lastfm_track_artist, 'lightblue'),
                    color(lastfm_track_album, 'lightblue'), tags, color(lastfm_track_playcount, 'green'))
            else:
                msg = "{0}'s last track: {1} by {2} from the album {3} {4}({5}) [playcount: {6}]".format(color(last_fm_track_user, 'green'),
                    color(lastfm_track_song, 'lightblue'), color(lastfm_track_artist, 'lightblue'),
                    color(lastfm_track_album, 'lightblue'), tags, lastfm_track_time, color(lastfm_track_playcount, 'green'))

        else:
            # user exists, track does not
            msg = "{0} has never listened to anything.".format(color(last_fm_track_user, 'green'))
    else:
        # user does not exist
        msg = "User {0} does not exist.".format(color(username, 'green'))

    line.conn.privmsg(line.args[0], msg)

@command("similar", man = "Obtain artists similar to the given artist. Usage: {leader}{command} <artist>")
def similar(bot, line):
    import json
    import requests
    from datetime import datetime
    from bot.colors import color

    SIMILAR_URL = "http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist={artist}&api_key={api_key}&format=json"
    API_KEY = bot.SECRETS["api_keys"]["lastfm"]

    artist = line.text

    if artist.strip() == "":
        line.conn.privmsg(line.args[0], "Please enter an artist.")
    else:
        similar_response = requests.get(SIMILAR_URL.format(artist=artist, api_key=API_KEY))
        similar_json = json.loads(similar_response.text)

        msg = ""
        i = 0

        if "similarartists" in similar_json:
            if "artist" in similar_json["similarartists"]:
                if similar_json["similarartists"]["@attr"]["artist"] == "[unknown]":
                    logging.warning("API Error: Unknown artist, but not Error code 6")
                    msg = "Artist {0} not found.".format(color(artist, 'green'))
                else:
                    msg = "Artists similar to {0}:".format(color(similar_json["similarartists"]["@attr"]["artist"], 'green'))
                    for a in similar_json["similarartists"]["artist"]:
                        if i < 8:
                            msg += " {0},".format(color(a["name"], 'lightblue'))
                            i += 1
            else:
                logging.warning("API Error: no ['artist'] key for {artist}".format(artist=artist))
        else:
            # Some sort of error in JSON
            if "error" in similar_json:
                if similar_json["error"] == 6:
                    msg = "Artist {0} not found.".format(color(artist, 'green'))
            logging.warning("API Error: no ['similarartists'] key for {artist}".format(artist=artist))
        line.conn.privmsg(line.args[0], msg[:-1] if msg[-1]==',' else msg)
