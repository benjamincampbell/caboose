import sqlite3
import re

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

def create_table(bot, table):
    c = bot.DB_CONN.cursor()
    print(table)
    cols = []
    sql = ("CREATE TABLE IF NOT EXISTS %s ("
           "id INTEGER PRIMARY KEY AUTOINCREMENT, " % t)
    for name, type in table.items():
        cols.append("%s %s" % (name, type))
    sql += ", ".join("?" * len(cols))
    sql += ")"
    print(sql)
    c.execute(sql, cols)
    bot.DB_CONN.commit()
    c.close()

def insert(bot, table_name, **values):
    # c = bot.DB_CONN.cursor()
    values = {k: v for k, v in values.items()}
    sql = "INSERT OR REPLACE INTO %s (" % table_name
    cols = []
    for c in values:
        cols.append(c)
    sql += ",".join(cols)
    sql += ") VALUES ("
    vals = []
    for key, value in values.items():
        vals.append(value)
    sql += ",".join("?" * len(vals))
    sql += ")"
    print(sql)
    print(vals)
    c = bot.DB_CONN.cursor()
    c.execute(sql, vals)
    bot.DB_CONN.commit()
    c.close()

def get_equal(bot, table_name, **conditions):
    values = {k: v for k, v in conditions.items()}
    sql = ("SELECT * "
           "FROM %s " % table_name)
    c = []
    vals = []

    if len(conditions) > 0:
        sql += "WHERE "
        for col, val in conditions.items():
            c.append("%s=?" % col)
            vals.append(val)
        sql += " AND ".join(c)
        print(sql)
        print(vals)

    c = bot.DB_CONN.cursor()
    result = c.execute(sql, vals).fetchall()
    c.close()
    return result

def delete(bot, table_name, **conditions):
    values = {k: v for k, v in conditions.items()}
    sql = ("DELETE "
           "FROM %s " % table_name)
    c = []
    vals = []

    if len(conditions) > 0:
        sql += "WHERE "
        for col, val in conditions.items():
            c.append("%s=?" % col)
            vals.append(val)
        sql += " AND ".join(c)
        print(sql)
        print(vals)

    c = bot.DB_CONN.cursor()
    result = c.execute(sql, vals).fetchall()
    c.close()
