import glob
import os

class cmd(object):
    #basic command object, holds the command itself (func) and any special options such as man (opts)
    def __init__(self, func, opts):
        self.func = func
        self.opts = opts

    def __call__(self, *argv):
        #python magic so calling the cmd object instance returns the function itself
        return self.func(*argv)
    
    def __getattr__(self, name):
        return self.opts[name]

def command(name, **options):
    """ Command format example:
    @command("echo", man = "Repeats back what is said. Syntax: " + handler.LEADER + "echo message")
    def echo(nick, channel, message, handler):
        handler.privmsg(channel, message)
    """
    def decorator(function):
        global commands
        commands[name] = cmd(function, options)
        return function
    return decorator

def reload_commands():
    print("Attempting to reload commands...")
    global commands
    commands = {}
    command_files = glob.glob(os.path.join("plugins", "*.py"))
    for source in command_files:
        print("Loading {0}".format(source))
        exec(compile(open(source, "U").read(), source, "exec"))
    return commands