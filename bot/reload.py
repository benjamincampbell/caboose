import glob
import os

def command(name, **options):
    def decorator(function):
        options['function'] = function
        commands[name] = options
        return function
    return decorator

def reload_commands():
    print("Attempting to reload commands...")
    global commands
    commands = {}
    command_files = glob.glob(os.path.join("plugins", "*.py"))
    for source in command_files:
        print("Loading {0}".format(source))
        exec(compile(open(source, "U").read(), source, "exec"), commands)
    return commands