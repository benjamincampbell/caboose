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
        #reload
        chamber = ['click','click','click','click','click','bang']
        handler.kick(channel, nick, result)
    else:
        #remove one click
        handler.privmsg(channel, '{}: {}'.format(nick, result))
        chamber.remove('click')
        print("click removed")
        print(chamber)