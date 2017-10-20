from bot.command import command

team_colors = {
    'arizona': ('white', 'red'),
    'atlanta': ('black', 'red'),
    'baltimore': ('white', 'magenta'),
    'buffalo': ('red', 'lightblue'),
    'carolina': ('black', 'lightcyan'),
    'chicago': ('orange', 'blue'),
    'cincinnati': ('black', 'orange'),
    'cleveland': ('orange', 'brown'),
    'dallas': ('blue', 'lightgrey'),
    'denver': ('blue', 'orange'),
    'detroit': ('lightgrey', 'lightblue'),
    'green bay': ('yellow', 'green'),
    'houston': ('red', 'blue'),
    'indianapolis': ('white', 'blue'),
    'jacksonville': ('white', 'cyan'),
    'kansas city': ('white', 'red'),
    'los angeles': ('yellow', 'blue'),
    'miami': ('orange', 'lightcyan'),
    'minnesota': ('yellow', 'magenta'),
    'new england': ('white', 'blue'),
    'new orleans': ('orange', 'black'),
    'ny giants': ('red', 'lightblue'),
    'ny jets': ('white', 'green'),
    'oakland': ('white', 'black'),
    'philadelphia': ('white', 'green'),
    'pittsburgh': ('yellow', 'black'),
    'san francisco': ('brown', 'red'),
    'seattle': ('lightcyan', 'blue'),
    'tampa bay': ('lightgrey', 'red'),
    'tennessee': ('lightcyan', 'blue'),
    'washington': ('white', 'brown'),
}

abbr = {
    'arizona': 'ari',
    'atlanta': 'atl',
    'baltimore': 'bal',
    'buffalo': 'buf',
    'carolina': 'car',
    'chicago': 'chi',
    'cincinnati': 'cin',
    'cleveland': 'cle',
    'dallas': 'dal',
    'denver': 'den',
    'detroit': 'det',
    'green bay': 'gb',
    'houston': 'hou',
    'indianapolis': 'ind',
    'jacksonville': 'jax',
    'kansas city': 'kc',
    'los angeles': 'la',
    'miami': 'mia',
    'minnesota': 'min',
    'new england': 'ne',
    'new orleans': 'no',
    'ny giants': 'nyg',
    'ny jets': 'nyj',
    'oakland': 'oak',
    'philadelphia': 'phi',
    'pittsburgh': 'pit',
    'san francisco': 'sf',
    'seattle': 'sea',
    'tampa bay': 'tb',
    'tennessee': 'ten',
    'washington': 'was',
}

@command("nflbox", man="Gets the box score of the current/upcoming game for an NFL team. Usage: {leader}{command} <city>  *(except 'ny jets' and 'ny giants') ")
def nflbox(bot, line):
    from plugins.espn_api import get_scores
    from bot.colors import color
    from plugins.nfl import abbr, team_colors
        
    ret = ""
    score = get_scores('nfl', line.text)
    if score != {}:
        for key, value in score.items():
            ret += "{t}: {s} @ ".format(t=color(abbr[value[0].lower()].upper(), *team_colors[value[0].lower()]), s=value[1])
            ret += "{t}: {s} ".format(t=color(abbr[value[2].lower()].upper(), *team_colors[value[2].lower()]), s=value[3])
            ret += value[4]
        line.conn.privmsg(line.args[0], ret)
        
@command("nflplayer" man="Get the stats of a given player name. Usage: {leader}{command} <firstname> <lastname>")
nflplayer(bot, line):
    import nflgame
    
    name = line.text
    players = nflgame.find(name)
    for p in players:
    