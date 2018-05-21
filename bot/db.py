import sqlite3

def get_db():
    conn = sqlite3.connect("caboose.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_tables(bot, tables):
    c = bot.DB_CONN.cursor()
    print(tables)
    for t in tables:
        print(t)
        cols = []
        sql = ("CREATE TABLE IF NOT EXISTS %s ("
               "id INTEGER PRIMARY KEY AUTOINCREMENT, " % t)
        for name, type in tables[t].items():
            cols.append("%s %s" % (name, type))
        sql += ", ".join(cols)
        sql += ")"
        print(sql)
        c.execute(sql)
    bot.DB_CONN.commit()
    c.close()

def insert(bot, table_name, **values):
    """
    TODO: this
    set(Bot, "setdata", nick="twitch", value="some value")
    ->
    INSERT INTO setdata
    (nick, value)
    VALUES
    ("twitch", "some value")
    """

def insert_or_replace(bot, table_name, **values):
    """
    TODO: make this
    """

def get_equal(bot, table_name, **conditions):
    sql = ("SELECT * "
           "FROM %s " % table_name)

    if len(conditions) > 0:
        sql += "WHERE "
        c = []
        for col, val in conditions.items():
            c.append("%s='%s'" % (col, val))
        sql += " AND ".join(c)
        print(sql)

    c = bot.DB_CONN.cursor()
    result = c.execute(sql).fetchall()
    c.close()
    return result
