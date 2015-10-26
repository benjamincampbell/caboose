import glob
import os

class cmd(object):
    def __init__(self, func, opts):
        self.func = func
        self.opts = opts

    def __call__(self, *argv):
        return self.func(*argv)
    
    def __getattr__(self, name):
        return self.opts[name]

def command(name, **options):
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