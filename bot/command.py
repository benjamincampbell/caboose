import glob
import os
import logging

class cmd(object):
    #basic command object, holds the command itself (func) and any special options such as man (opts)
    def __init__(self, func, opts):
        self.func = func
        self.opts = opts
        self.visible = True
        self.enabled = True

    def __call__(self, *argv):
        #python magic so calling the cmd object instance returns the function itself
        return self.func(*argv)

    def __getattr__(self, name):
        return self.opts[name]

    def toggle_visible(self):
        if self.visible:
            self.visible = False
            return False
        else:
            self.visible = True
            return True

    def toggle_enabled(self):
        if self.enabled:
            self.enabled = False
            return False
        else:
            self.enabled = True
            return True

def command(name, **options):
    """ Command format example:
    @command("echo", man = "Repeats back what is said. Syntax: " + bot.LEADER + "echo message")
    def echo(nick, channel, message, bot):
        bot.privmsg(channel, message)
    """
    def decorator(function):
        global commands
        commands[name] = cmd(function, options)
        if "aliases" in options:
            for a in options["aliases"]:
                commands[a] = commands[name]
        return function
    return decorator

# This method needed to be defined in this file, else the tables variable
# could not be found
def db(**columns):
    def decorator(function):
        global tables
        tables[function.__name__] = columns
        return function
    return decorator

def reload_commands():
    #Loads all *.py files in plugins/ into cmd objects in the global commands dictionary
    logging.info("Reloading commands")
    global commands
    commands = {}
    global tables
    tables = {}
    command_files = glob.glob(os.path.join("plugins", "*.py"))
    for source in command_files:
        logging.info("Loading {0}".format(source))
        with open(source, 'r') as f:
            exec(compile(f.read(), source, "exec"))
    return commands, tables

def decorate_mans(leader, commands):
    for key, command in commands.items():
        commands[key].man = commands[key].man.format(leader=leader, command=key)
