@command("roulette", man = "Play Russian Roulette in channels where Caboose has ops. Usage: {leader}{command}")
def roulette(bot, line):
    import random

    #chamber needs to persist through function calls without making a new one each time
    global chamber

    try:
        chamber
    except NameError:
        #Only make a new chamber if chamber is uninitialized, after reboot
        chamber = ['click','click','click','click','click','bang']
    else:
        pass

    result = random.choice(chamber)

    if result == 'bang':
        if random.randint(1, 100) > 1:
            #reload
            chamber = ['click','click','click','click','click','bang']
            line.conn.kick(line.args[0], line.user.nick, result)
            line.conn.privmsg(line.args[0], 'reloading...')
        else:
            #misfire! 1/100 chance to not fire. lucked out!
            chamber = ['click','click','click','click','click','bang']
            line.conn.privmsg(line.args[0], '{}: misfire! reloading...'.format(line.user.nick))
            line.conn.privmsg('twitch', '{} got a misfire! lucky!'.format(line.user.nick))
    else:
        #remove one click
        line.conn.privmsg(line.args[0], '{}'.format(result))
        chamber.remove('click')