@command("nfl", man="Gets information about an NFL team. Usage: {leader}{command} <team>")
def nfl(bot, line):
    from plugins.espn_api import get_scores
    from bot.colors import color
        
    team_colors = {
        'arizona': ('white', 'red'),
        'atlanta': ('black', 'red'),
        'baltimore': ('white', 'magenta'),
        'buffalo': ('red', 'lightblue'),
        'chicago': ('orange', 'blue'),
        'cincinnati': ('black', 'orange'),
        'cleveland': ('white', 'orange'),
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

    
    ret = ""
    score = get_scores('nfl', line.text)
    if score != {}:
        for key, value in score.items():
            ret += "{t}: {s} | ".format(t=color(abbr[value[0].lower()].upper(), team_colors[value[0].lower()][0], team_colors[value[0].lower()][1]), s=value[1])
            ret += "{t}: {s} ".format(t=color(abbr[value[2].lower()].upper(), team_colors[value[2].lower()][0], team_colors[value[2].lower()][1]), s=value[3])
            ret += value[4]
        line.conn.privmsg(line.args[0], ret)