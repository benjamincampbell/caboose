from bot.command import command, db

@command("setdata", man="sets arbitrary data for a user")
@db(nick="TEXT UNIQUE", value="TEXT")
def setdata(bot, line):
    from bot.db import insert

    nick = line.user.nick
    value = line.text

    insert(bot, "setdata", nick=nick, value=value)

    line.conn.privmsg(line.args[0], "value {val} set for nick {nick}".format(val=value,
                                                                             nick=nick))

@command("getdata", man="gets data of user")
def getdata(bot, line):
    import random
    from bot.db import get_equal

    nick = line.text
    results = get_equal(bot, "setdata", nick=nick)

    if len(results) > 0:
        result = random.choice(results)
    else:
        result = {
            "nick": line.text,
            "value": "No value existed"
        }

    print(result)

    # c = bot.DB_CONN.cursor()
    # result = c.execute(sql).fetchone()
    # c.close()

    line.conn.privmsg(line.args[0], "nick: {0} | value: {1}".format(result["nick"], result["value"]))
