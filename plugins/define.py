from bot.command import command

@command("define", aliases = ['def'], man = "Repeats back what is said. Usage: {leader}{command} <message>")
def define(bot, line):
    import random

    from bot.colors import color

    if len(line.text.split()) != 1:
        line.conn.privmsg(line.args[0], "Please enter only one word.")
    else:
        try:
            word = bot.dictionary.meaning(line.text.strip())
            response = line.text.strip()

            for k, v in word.items():
                i = random.randint(0, len(v)-1)
                response += " ({0}): {1}".format(color(k, 'lightblue'), v[i])

                if k != list(word.keys())[-1]:
                    response += " |"

            line.conn.privmsg(line.args[0], response)
        except AttributeError as e:
            line.conn.privmsg(line.args[0], "No definition found for '{0}'".format(line.text.strip()))
