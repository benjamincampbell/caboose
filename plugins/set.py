from bot.command import command, db

@command("setdata", man="sets arbitrary data for a user")
@db(nick="TEXT", value="TEXT")
def setdata(bot, line):

    nick = line.user.nick
    value = line.text.replace("\'", "''")

    sql = """
        INSERT INTO setdata
        (nick, value)
        VALUES
        ('%s', '%s')
    """ % (nick, value)

    print(sql)

    c = bot.DB_CONN.cursor()
    result = c.execute(sql)
    bot.DB_CONN.commit()
    c.close()

    line.conn.privmsg(line.args[0], "value {val} set for nick {nick}".format(val=value,
                                                                             nick=nick))

@command("getdata", man="gets data of user")
def getdata(bot, line):
    import random
    from bot.db import get_equal

    sql = """
          SELECT * FROM setdata
          """

    nick = line.text
    results = get_equal(bot, "setdata", nick=nick)

    result = random.choice(results)

    print(result)

    # c = bot.DB_CONN.cursor()
    # result = c.execute(sql).fetchone()
    # c.close()

    line.conn.privmsg(line.args[0], "nick: {0} | value: {1}".format(result["nick"], result["value"]))
