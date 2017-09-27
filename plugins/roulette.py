@command("roulette", man = "Play Russian Roulette in channels where Caboose has ops. Usage: &roulette")
def roulette(nick, channel, message, bot):
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
            bot.kick(channel, nick, result)
            bot.privmsg(channel, 'reloading...')
        else:
            #misfire! 1/100 chance to not fire. lucked out!
            chamber = ['click','click','click','click','click','bang']
            bot.privmsg(channel, '{}: misfire! reloading...'.format(nick))
            bot.privmsg('twitch', '{} got a misfire! lucky!'.format(nick))
    else:
        #remove one click
        bot.privmsg(channel, '{}'.format(result))
        chamber.remove('click')
        print("click removed")
        print(chamber)
