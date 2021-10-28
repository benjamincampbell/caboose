import requests
import logging
import json
from datetime import datetime

from bot.colors import color
from bot.command import command, db

# TODO: Add year to album of song; The Colour and the Shape (1997)

def api_errors(e):
    errors = {
        "2" : "Invalid service - This service does not exist",
        "3" : "Invalid Method - No method with that name in this package",
        "4" : "Authentication Failed - You do not have permissions to access the service",
        "5" : "Invalid format - This service doesn't exist in that format",
        "6" : "Invalid parameters - Your request is missing a required parameter",
        "7" : "Invalid resource specified",
        "8" : "Operation failed - Something else went wrong",
        "9" : "Invalid session key - Please re-authenticate",
        "10" : "Invalid API key - You must be granted a valid key by last.fm",
        "11" : "Service Offline - This service is temporarily offline. Try again later.",
        "13" : "Invalid method signature supplied",
        "16" : "There was a temporary error processing your request. Please try again",
        "26" : "Suspended API key - Access for your account has been suspended, please contact Last.fm",
        "29" : "Rate limit exceeded - Your IP has made too many requests in a short period",
    }
    return errors[e]

@command("lastfm", aliases=["nowplaying", "lfm", "np"], man="Obtains most recently played song for a given Last.fm user. "
        "-default to set default user for your nick, to use if no username given. "
        "Usage: {leader}{command} [-default] <username>")
@db(nick="STRING UNIQUE", username="STRING")
def lastfm(bot, line):
    from bot.colors import color
    from bot.db import insert, get_equal
    from plugins.lastfm import get_last_played_track

    # testing
    # import pprint

    API_KEY = bot.SECRETS["api_keys"]["lastfm"]

    parts = line.text.split(' ')

    if parts[0] == "-default":
        # set default username for the nick calling the function
        if len(parts[1:]) != 1:
            # make sure they're actually providing an argument
            line.conn.privmsg(line.args[0], "Please enter a one-word username.")
            return None

        username = parts[1]

        if username == "":
            line.conn.privmsg(line.args[0], "Please enter an alphanumeric username.")
            return None
        else:
            # insert the username into the table
            insert(bot, "lastfm", nick=line.user.nick, username=username)
            line.conn.privmsg(line.args[0], "Default username {0} set for {1}".format(color(username, 'green'), line.user.nick))
    else:
        # look up given nickname, or default for user if there is no given username.
        if parts[0] != "":
            # Some argument was given after !lastfm
            if len(parts) > 1:
                # Usernames are 1 word, not >=2
                line.conn.privmsg(line.args[0], "Please enter a one-word username.")
                return None
            username = parts[0]
        else:
            # no username given, try to use default
            try:
                result = get_equal(bot, "lastfm", nick=line.user.nick)[0]
                username = result["username"]
            except IndexError:
                # no row found, username not in table
                line.conn.privmsg(line.args[0], "No username given, nor a default for {nick} found.".format(nick=line.user.nick))
                return None

        msg = get_last_played_track(username, API_KEY)

        line.conn.privmsg(line.args[0], msg)

def get_last_played_track(username, api_key):
    RECENT_TRACK_URL = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={user}&api_key={api_key}&format=json"
    TRACK_INFO_URL = "http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key={api_key}&artist={artist}&track={track}&username={user}&format=json"

    recent_response = requests.get(RECENT_TRACK_URL.format(user=username, api_key=api_key))

    try:
        recent_json = json.loads(recent_response.text)
    except ValueError:
        logger.severe("Error parsing response: {response}".format(response=recent_response))
        line.conn.privmsg(line.args[0], "Error parsing JSON response")
        return None

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
            # pp = pprint.PrettyPrinter(indent=4)
            # pp.pprint(lastfm_track_info)

            lastfm_track_song = lastfm_track_info["name"]
            lastfm_track_artist = lastfm_track_info["artist"]["#text"]
            lastfm_track_album = lastfm_track_info["album"]["#text"]

            try:
                lastfm_track_time = lastfm_track_info["@attr"]["nowplaying"]
                now_playing = True
            except KeyError:
                lastfm_track_time = lastfm_track_info["date"]["#text"]
                now_playing = False

            track_info_response = requests.get(TRACK_INFO_URL.format(api_key=api_key, artist=lastfm_track_artist,
                track=lastfm_track_song, user=last_fm_track_user))
            track_info_json = json.loads(track_info_response.text)

            last_fm_track_tags = []

            try:
                lastfm_track_playcount = track_info_json["track"]["userplaycount"]
                track_info_exists = True
                last_fm_track_tags = track_info_json["track"]["toptags"]["tag"]
            except KeyError:
                track_info_exists = False
                lastfm_track_playcount = "0"

            # pp.pprint(track_info_json)

            if (last_fm_track_tags == []):
                tags = ""
            else:
                tags = "({0}) ".format(", ".join(t["name"] for t in last_fm_track_tags))

            if now_playing:
                msg = "{0} is listening to {1} by {2} from the album {3} {4}[playcount: {5}]".format(
                    color(last_fm_track_user, 'green'),
                    color(lastfm_track_song, 'lightblue'),
                    color(lastfm_track_artist, 'lightblue'),
                    color(lastfm_track_album, 'lightblue'),
                    tags,
                    color(lastfm_track_playcount, 'green'))
            else:
                msg = "{0}'s last track: {1} by {2} from the album {3} {4}({5}) [playcount: {6}]".format(
                    color(last_fm_track_user, 'green'),
                    color(lastfm_track_song, 'lightblue'),
                    color(lastfm_track_artist, 'lightblue'),
                    color(lastfm_track_album, 'lightblue'),
                    tags, lastfm_track_time,
                    color(lastfm_track_playcount, 'green'))

        else:
            # user exists, track does not
            msg = "{0} has never listened to anything.".format(color(last_fm_track_user, 'green'))
    else:
        # user does not exist
        msg = "User {0} does not exist.".format(color(username, 'green'))
    return msg

@command("similar", man="Obtain artists similar to the given artist. Usage: {leader}{command} <artist>")
def similar(bot, line):
    import json
    import requests
    import logging
    from bot.colors import color
    from plugins.lastfm import api_errors

    SIMILAR_URL = "http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist={artist}&api_key={api_key}&format=json"
    API_KEY = bot.SECRETS["api_keys"]["lastfm"]
    logger = logging.getLogger("log")

    artist = line.text

    if artist.strip() == "":
        line.conn.privmsg(line.args[0], "Please enter an artist.")
    else:
        similar_response = requests.get(SIMILAR_URL.format(artist=artist, api_key=API_KEY))
        similar_json = json.loads(similar_response.text)

        msg = ""
        artist_list = []

        if "similarartists" in similar_json:
            if "artist" in similar_json["similarartists"]:
                if similar_json["similarartists"]["@attr"]["artist"] == "[unknown]":
                    logger.warning("API Error: Unknown artist, but not Error code 6")
                    msg = "Artist {0} not found.".format(color(artist, 'green'))
                else:
                    msg = "Artists similar to {0}:".format(color(similar_json["similarartists"]["@attr"]["artist"], 'green'))
                    for a in similar_json["similarartists"]["artist"]:
                        if len(artist_list) < 8:
                            artist_list.append(a["name"])
                    msg += ",".join(map(lambda x: color(" "+x, 'lightblue'), artist_list))
            else:
                logger.warning("API Error: no ['artist'] key for {artist}".format(artist=artist))
        else:
            # Some sort of error in JSON
            if "error" in similar_json:
                msg = "API Error: artist not found."
                logger.warning(api_errors(str(similar_json["error"])))
            logger.warning("API Error: no ['similarartists'] key for {artist}".format(artist=artist))
        line.conn.privmsg(line.args[0], msg)

@command(name="tags", aliases=["genre","genres"], man="Get the top tags for a given artist. Usage: {leader}{command} <artist>")
def tags(bot, line):
    import json
    import requests
    import logging
    from bot.colors import color
    from plugins.lastfm import api_errors

    ARTIST_TAGS_URL = "http://ws.audioscrobbler.com/2.0/?method=artist.gettoptags&artist={artist}&api_key={api_key}&format=json"
    API_KEY = bot.SECRETS["api_keys"]["lastfm"]
    logger = logging.getLogger("log")

    ignore_tags = [
            "seen live",
            "seenlive",
            "seen",
            "live",
            "england",
            "uk",
            "britain",
            "british",
            "english"
            ]

    msg = ""
    artist = line.text

    if artist.strip() == "":
        line.conn.privmsg(line.args[0], "Please enter an artist.")
    else:
        tags_response = requests.get(ARTIST_TAGS_URL.format(artist=artist, api_key=API_KEY))
        tags_json = json.loads(tags_response.text)

        msg = ""
        tag_list = []

        if "toptags" in tags_json:
            if "tag" in tags_json["toptags"]:
                if tags_json["toptags"]["@attr"]["artist"] == "[unknown]":
                    logger.warning("API Error: Unknown artist, but not Error code 6")
                    msg = "Artist {0} not found.".format(color(artist, 'green'))
                else:
                    if not tags_json["toptags"]["tag"]:
                        msg = "No tags found for artist {artist}".format(
                            artist=color(artist, 'green')
                        )
                    else:
                        msg = "Top tags for {0}:".format(color(tags_json["toptags"]["@attr"]["artist"], 'green'))
                        for t in tags_json["toptags"]["tag"]:
                            if len(tag_list) < 8 and t["name"].lower() not in ignore_tags:
                                tag_list.append(t["name"])
                        msg += ",".join(map(lambda x: color(" "+x, 'lightblue'), tag_list))
            else:
                logger.warning("API Error: no ['tag'] key for {artist}".format(artist=artist))
        else:
            # Some sort of error in JSON
            if "error" in tags_json:
                msg = "API Error: artist not found"
                logger.warning(api_errors(str(tags_json["error"])))
            logger.warning("API Error: no ['toptags'] key for {artist}".format(artist=artist))
        line.conn.privmsg(line.args[0], msg)


# TODO: add feature to enqueue a # of creeps, no repeats. I.e. !mc 3 to creep on 3 people in a row, no repeats.
@command("musiccreep", aliases=["creep", "mc"], man="Obtain the last-played song of a random user who has a default "
        "Last.fm username set via !lastfm. Optionally supply number to enqueue creeps. Usage: {leader}{command} <number>")
def musiccreep(bot, line):
    import random
    import time
    from bot.db import get_equal
    from plugins.lastfm import get_last_played_track


    API_KEY = bot.SECRETS["api_keys"]["lastfm"]
    num = 1

    linesplit = line.text.split()
    if len(linesplit) > 1:
        # too many arguments
        line.conn.privmsg(line.user.nick, "Too many arguments supplied")
        return None
    elif len(linesplit) == 1:
        if linesplit[0].isdigit() and int(linesplit[0]) < 6:
            num = int(linesplit[0])
        else:
            line.conn.privmsg(line.user.nick, "Please enter a number 5 or fewer.")

    # else no args

    results = get_equal(bot, "lastfm")

    if num > len(results):
        num = len(results)

    choices = random.sample(results, num)

    print(choices)
    for u in choices:
        username = u["username"]
        msg = get_last_played_track(username, API_KEY)

        line.conn.privmsg(line.args[0], msg)
        time.sleep(2)

def get_artists_for_tag(tag, api_key):
    TAG_URL="http://ws.audioscrobbler.com/2.0/?method=tag.gettopartists&tag={tag}&api_key={api_key}&format=json&limit=269"

    tag_response = requests.get(TAG_URL.format(tag=tag, api_key=api_key))
    tag_json = json.loads(tag_response.text)
    logger = logging.getLogger("log")

    msg = ""
    full_artist_list = []

    if "topartists" in tag_json:
        if "artist" in tag_json["topartists"]:
            if tag_json["topartists"]["@attr"]["tag"] == "[unknown]":
                logger.warning("API Error: Unknown tag, but not Error code 6")
                raise Exception("Tag {0} not found.".format(color(tag, 'green')))
            else:
                if not tag_json["topartists"]["artist"]:
                    raise Exception("No artists found for tag {tag}".format(
                        tag=color(tag, 'green')
                    ))
                else:
                    full_artist_list = tag_json["topartists"]["artist"]
        else:
            logger.warning("API Error: no ['artist'] key for {tag}".format(tag=tag))
    else:
        # Some sort of error in JSON
        if "error" in tag_json:
            logger.warning(api_errors(str(tag_json["error"])))
            raise Exception("API Error: Artist not found")
        logger.warning("API Error: no ['topartists'] key for {tag}".format(tag=tag))
        raise Exception("API Error: no ['topartists'] key for {tag}".format(tag=tag))

    return full_artist_list


@command("topartists", aliases=["ta"], man="See the top artists for the given tag. Usage: {leader}{command}")
def topartists(bot, line):
    import json
    import requests
    import logging
    from bot.colors import color
    from plugins.lastfm import api_errors, get_artists_for_tag

    API_KEY = bot.SECRETS["api_keys"]["lastfm"]

    tag = line.text

    if tag.strip() == "":
        line.conn.privmsg(line.args[0], "Please enter a tag.")
        return None

    full_artist_list = get_artists_for_tag(tag, API_KEY)
    artist_list = []

    msg = "Top artists for {0}:".format(color(tag, 'green'))

    for a in full_artist_list:
        if len(artist_list) < 8:
            artist_list.append(a["name"])
    msg += ",".join(map(lambda x: color(" "+x, 'lightblue'), artist_list))

    line.conn.privmsg(line.args[0], msg)

@command("explore", aliases=["randomartist", "ra"], man="Get a random artists for the given tag. Usage: {leader}{command}")
def explore(bot, line):
    import json
    import requests
    import logging
    import random
    from bot.colors import color
    from plugins.lastfm import api_errors, get_artists_for_tag

    API_KEY = bot.SECRETS["api_keys"]["lastfm"]

    tag = line.text

    if tag.strip() == "":
        line.conn.privmsg(line.args[0], "Please enter a tag.")
        return None
    # try:
    full_artist_list = get_artists_for_tag(tag, API_KEY)
    artist = random.choice(full_artist_list)

    msg = "Like {tag}? Try {artist}".format(tag=color(tag, "green"), artist=color(artist["name"], "lightblue"))
    # except Exception as err:
    # msg = str(err)

    line.conn.privmsg(line.args[0], msg)

@command("plays", aliases=["p"], man="Get the number of plays of an artist for a given user. Usage: {leader}{command} <artist>")
def plays(bot, line):
    import logging
    import json
    import requests
    from bot.db import get_equal
    from bot.colors import color
    from plugins.lastfm import get_artist_plays_for_user
    
    logger = logging.getLogger("log")

    API_KEY = bot.SECRETS["api_keys"]["lastfm"]
    user = ""
    balls = 0

    try:
        result = get_equal(bot, "lastfm", nick=line.user.nick)[0]
        user = result["username"]
    except IndexError:
        line.conn.privmsg(line.args[0], "Please set a default username first.")
        return None
    
    artist = line.text

    if artist == "":
        line.conn.privmsg(line.args[0], "Please supply an artist.")
        return None
    
    balls = get_artist_plays_for_user(artist, user, API_KEY)

    msg = "{user} has listened to {artist} {playcount} times".format(user=color(user, "green"), artist=color(artist, "lightblue"), playcount=color(balls,"green"))

    line.conn.privmsg(line.args[0], msg)


def get_artist_plays_for_user(a,b,c):
    return "1"
"""
def get_artist_plays_for_user(artist, user, api_key):
    PLAYS_URL = "http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={artist}&api_key={api_key}&format=json&username={user}"
    
    response = requests.get(PLAYS_URL.format(artist=artist, api_key=api_key, user=user))

    balls = 0
 
    try:
        plays_json = json.loads(response.text)
    except ValueError:
        logger.severe("Error parsing response: {response}".format(response=response))
        line.conn.privmsg(line.args[0], "Error parsing JSON response")
        return None

    try:
        balls = plays_json["artist"]["stats"]["userplaycount"]
    except:
        line.conn.privmsg(line.args[0], "Something went wrong. Does this artist exist?")
        return None

    return balls
"""


@command("top", man="Get the top artists for a user in the given time frame. Usage: {leader}{command} [-w|-m|-3m|-y|-a] (<username>)")
def top(bot, line):
    import json
    import requests
    import logging
    from bot.db import insert, get_equal
    from bot.colors import color
    from plugins.lastfm import get_top_artists_for_user

    logger = logging.getLogger("log")
    # Example: !top -w twitch043    top artists of the last week for user twitch043
    #          !top -y              top artists of the last year for default user, else error
    #          !top twitch043       top artists of all time for user twitch043
    #          !top                 top artists of all time for default user, else error

    API_KEY = bot.SECRETS["api_keys"]["lastfm"]
    tag = ""
    user = ""
    artist_counts = []

    linesplit = line.text.split()

    for a in linesplit:
        if a[0] == '-':
            if a[1:] not in ["a", "w", "m", "3m", "y"]: # TODO: move time_periods up here, use keys
                line.conn.privmsg(line.args[0], "Not a valid argument")
                return None
            tag = a
        else:
            user = a

    if (tag == ""):
        # no tag, default to all time
        tag = "-a"

    if (user == ""):
        # supplied no user, obtain default user
        try:
            result = get_equal(bot, "lastfm", nick=line.user.nick)[0]
            user = result["username"]
        except IndexError:
            # no row found, username not in table
            line.conn.privmsg(line.args[0], "No username given, nor a default for {nick} found.".format(nick=line.user.nick))
            return None

    else:
        logger.warning("No tag nor username conditions matched for lastfm top")
        # something else?

    try:
        username, artist_counts = get_top_artists_for_user(API_KEY, user, tag)
    except TypeError:
        line.conn.privmsg(line.args[0], "Username not found")
        return None

    time_periods = {
        "-a":"all time",
        "-w":"last week",
        "-m":"last month",
        "-3m":"last three months",
        "-y":"last year"
    }

    msg = "{user}'s most played artists ({time_period}):".format(user=color(username, "green"), time_period=time_periods[tag])
    msg += ",".join(map(lambda x: color(" "+x[0], 'lightblue')+" ({})".format(x[1]), artist_counts))

    line.conn.privmsg(line.args[0], msg)

def get_top_artists_for_user(API_KEY, user, time_arg="-a"):
    logger = logging.getLogger("log")

    time_periods = {
        "-a":"overall",
        "-w":"7day",
        "-m":"1month",
        "-3m":"3month",
        "-y":"12month"
    }

    artist_counts = []

    period = time_periods[time_arg]

    TOP_ARTISTS_URL = "http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&api_key={api_key}&user={user}&period={time_period}&format=json"

    top_response = requests.get(TOP_ARTISTS_URL.format(api_key=API_KEY, user=user, time_period=period))
    top_json = json.loads(top_response.text)

    try:
        for artist in top_json["topartists"]["artist"]:
            if len(artist_counts) < 8:
                artist_counts.append((artist["name"], artist["playcount"]))
        username = top_json["topartists"]["@attr"]["user"]
        return (username, artist_counts)
    except KeyError:
        logger.warning("API Error. JSON: {json}".format(json=top_json))
