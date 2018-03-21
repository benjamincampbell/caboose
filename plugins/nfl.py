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

def passing_stats(pstats):
    return "{}/{} for {} yds, {} TD, {} INT".format(pstats.passing_cmp,
                                                      pstats.passing_att,
                                                      pstats.passing_yds,
                                                      pstats.passing_tds,
                                                      pstats.passing_ints)

def rushing_stats(pstats):
    ret = "{} rushes for {} yds (long {}), {} TD ".format(pstats.rushing_att,
                                                           pstats.rushing_yds,
                                                           pstats.rushing_lng,
                                                           pstats.rushing_tds)
    if (pstats.rushing_att > 0):
        ret += "({} avg)".format(pstats.rushing_yds / pstats.rushing_att)
    else:
        ret += "(0.0 avg)"
    return ret

def receiving_stats(pstats):
    ret = "{} catches for {} yds (long {}), {} TD ".format(pstats.receiving_rec,
                                                                    pstats.receiving_yds,
                                                                    pstats.receiving_lng,
                                                                    pstats.receiving_tds)
    if (pstats.receiving_rec > 0):
        ret += "({} avg)".format(pstats.receiving_yds / pstats.receiving_rec)
    else:
        ret += "(0.0 avg)"
    return ret

def det_stats(pstats):
    pos = pstats.guess_position
    s = ""
    
    if (pos == 'QB'):
        s += passing_stats(pstats)
        if (pstats.rushing_att > 0):
            s += " | " + rushing_stats(pstats)
    if (pos == 'RB'):
        s += rushing_stats(pstats) + " | " + receiving_stats(pstats)
    if (pos == 'WR'):
        s += receiving_stats(pstats)
        if (pstats.rushing_att > 0):
            s += " | " + rushing_stats(pstats)
    if (pos == 'TE'):
        s += receiving_stats(pstats)
        
    return s

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
        
@command("nflplayer", man="Get the stats of a given player name. Usage: {leader}{command} [-year=<year>] [-week=<week>] <firstname> <lastname>")
def nflplayer(bot, line):
    import nflgame
    from datetime import date
    from plugins.nfl import det_stats
    import collections
    
    nflgame.live._update_week_number()    
    
    name = ' '.join(line.text.split(' ')[-2:])
    players = nflgame.find(name)
    year = False
    week = False
    y = nflgame.live._cur_year
    w = nflgame.live._cur_week
    
    parts = collections.deque(line.text.split(' '))
    for p in parts:
        if p.startswith('-year'):
            year = True
            y = p.split('=')[1]
        if p.startswith('-week'):
            week = True
            w = p.split('=')[1]
            
    
    for p in players:
        ret = ""
        
        print(p.name)
        print(year)
        print(y)
        print(week)
        print(w)
        try:
            if year and not week:
                pstats = p.stats(y)
            else:
                pstats = p.stats(y, w)
            ret += str(p) + " - "
            ret += det_stats(pstats)
            line.conn.privmsg(line.args[0], ret)
        except TypeError:
            line.conn.privmsg(line.args[0],
                              "Could not find games for player {}".format(' '.join(line.text.split(' ')[-2:])))

    """
    Aaron Rodgers (QB, GB) - 25/30 for 300 yds, 3 TD, 0 INT | 4 rushes for 40 yds (10.0 avg)
    Ty Montgomery (RB, GB) - 14 rushes for 70 yds, 1 TD (5.0 avg) | 5 catches for 30 yds (6.0 avg)
    """
        
    