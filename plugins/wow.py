from bot.command import command
from bot.colors import color

def classes(c):
    classes = {
        "1": ("Warrior", "brown"),
        "2": ("Paladin", "pink"),
        "3": ("Hunter", "lightgreen"),
        "4": ("Rogue", "yellow"),
        "5": ("Priest", "white"),
        "6": ("Death Knight", "red"),
        "7": ("Shaman", "lightblue"),
        "8": ("Mage", "lightcyan"),
        "9": ("Warlock", "blue"),
        "10": ("Monk", "green"),
        "11": ("Druid", "orange"),
        "12": ("Demon Hunter", "magenta")
    }
    return classes[c]

def races(r):
    races = {
        "1": "Human",
        "2": "Orc",
        "3": "Dwarf",
        "4": "Night Elf",
        "5": "Undead",
        "6": "Tauren",
        "7": "Gnome",
        "8": "Troll",
        "9": "Goblin",
        "10": "Blood Elf",
        "11": "Draenei",
        "22": "Worgen",
        "24": "Pandaren",
        "25": "Pandaren",
        "26": "Pandaren",
        "27": "Nightborne",
        "28": "Highmountain Tauren",
        "29": "Void Elf",
        "30": "Lightforged Draenei"
    }
    return races[r]

def genders(g):
    genders = {
        "0": "Male",
        "1": "Female"
    }
    return genders[g]

def factions(f):
    factions = {
        "0": "Alliance",
        "1": "Horde"
    }
    return factions[f]

@command("wow", man="Obtain information about a World of Warcraft character. Usage: {leader}{command} <realm> <character>")
def lastfm(bot, line):
    import json
    import requests
    import logging
    from bot.colors import color
    from plugins.shorten import shorten_url
    from plugins.wow import classes, races, genders, factions

    WOW_CHAR_URL = "https://us.api.battle.net/wow/character/{realm}/{character}?fields=items+talents&locale=en_US&apikey={api_key}"
    PROFILE_URL = "https://worldofwarcraft.com/en-us/character/{realm}/{character}"
    API_KEY = bot.SECRETS["api_keys"]["blizzard"]

    parts = line.text.split(' ')

    if len(parts) < 2:
        line.conn.privmsg(line.args[0], "Please enter a realm and character name")
    else:
        # Realms can be 1-3 words, so character is the last word, realm is the rest
        char = parts[-1]
        server = " ".join(parts[:-1])

        wow_response = requests.get(WOW_CHAR_URL.format(realm=server, character=char, api_key=API_KEY))
        try:
            wow_json = json.loads(wow_response.text)
        except ValueError:
            line.conn.privmsg(line.args[0], "API Error")
            return None

        msg = ""

        if "status" in wow_json:
            if wow_json["status"] == "nok":
                msg = "Character not found, make sure to use !wow <realm> <character>"
        else:
            try:
                name = color(wow_json["name"], "green")
                realm = color(wow_json["realm"], "lightblue")
                level = color(wow_json["level"], "yellow")
                ilvl = color(wow_json["items"]["averageItemLevel"], "yellow")
                gender = genders(str(wow_json["gender"]))
                race = races(str(wow_json["race"]))
                raw_class, class_color = classes(str(wow_json["class"]))
                _class = color(raw_class, class_color)
                spec = color(wow_json["talents"][0]["spec"]["name"], class_color)
                faction = factions(str(wow_json["faction"]))
                points = wow_json["achievementPoints"]
                kills = wow_json["totalHonorableKills"]
                url = shorten_url(bot, PROFILE_URL.format(realm=server.replace(' ', '-'),
                                                          character=char))

                msg = ("{n} is a Level {l} (ilvl {i}) {g} {r} {s} {c} in"
                       " realm {re}, with {k} Honorable Kills "
                       "({u})").format(n=name,
                                       l=level,
                                       i=ilvl,
                                       g=gender,
                                       r=race,
                                       s=spec,
                                       c=_class,
                                       re=realm,
                                       k=kills,
                                       u=url)
            except Exception as e:
                msg = "An error occured"
                logging.warning(e)
        line.conn.privmsg(line.args[0], msg)
