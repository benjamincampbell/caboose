@command("roulette", man = "Play Russian Roulette in channels where Caboose has ops. Usage: &roulette")
def roulette(nick, channel, message, handler):
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
        if random.randint(1, 100) < 1:
            #reload
            chamber = ['click','click','click','click','click','bang']
            handler.kick(channel, nick, result)
            handler.privmsg(channel, 'reloading...')
        else:
            #misfire! 1/100 chance to not fire. lucked out!
            chamber = ['click','click','click','click','click','bang']
            handler.privmsg(channel, '{}: misfire! reloading...')
    else:
        #remove one click
        handler.privmsg(channel, '{}: {}'.format(nick, result))
        chamber.remove('click')
        print("click removed")
        print(chamber)