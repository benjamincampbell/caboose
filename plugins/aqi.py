from bot.command import command

@command("aqi", aliases = ["aqi"], man = "Returns aqi information about an area: {leader}{command} [location]")
@db(nick="STRING UNIQUE", location="string")
def aqi(bot, line):
    import random
    import logging
    import ozon3 as ooo
    from bot.colors import color
    from bot.db import insert, get_equal

    API_KEY = bot.SECRETS["api_keys"]["ozon3"]
    parts = line.text.split(' ')

    if parts[0] == "-default":
        location = parts[1:]
        location = " ".join(map(str, location))
        if location == "":
            line.conn.privmsg(line.args[0], "Please enter a valid location.")
            return None
        else:
            # insert the username into the table
            insert(bot, "aqi", nick=line.user.nick, location=location)
            line.conn.privmsg(line.args[0], "Default location {0} set for {1}".format(color(location, 'green'), line.user.nick))

    else:
        try:
            if parts[0] != "":
                location = line.text
            else:
                # no username given, try to use default
                try:
                    result = get_equal(bot, "aqi", nick=line.user.nick)[0]
                    location = result["location"]
                except IndexError:
                    # no row found, username not in table
                    line.conn.privmsg(line.args[0], "No location given, nor a default for {nick} found. Set one with !aqi -default [location]".format(nick=line.user.nick))
                    return None

            o3 = ooo.Ozon3(API_KEY)
            data = o3.get_city_air(location)
            aqi = int(data.aqi[0])
            print(data.aqi[0])
            if aqi < 34:
                textColor = 'lightblue'
            elif aqi < 67:
                textColor = 'green'
            elif aqi < 100:
                textColor = 'yellow'
            elif aqi < 150:
                textColor = 'orange'
            elif aqi < 200:
                textColor = 'magenta'
            else:
                textColor = 'red'

            line.conn.privmsg(line.args[0], "Current AQI in {0} is {1}".format(location, color(aqi, textColor)))
        except Exception as e:
            logger = logging.getLogger("log")
            logger.warning("Error: {0}".format(e))
