import glob
import os

def reload_commands():
    print("Attempting to reload commands...")
    global commands
    commands = {}
    command_files = glob.glob(os.path.join("plugins", "*.py"))
    for source in command_files:
        print("Loading {0}".format(source))
        exec(compile(open(source, "U").read(), source, "exec"), commands)
    return commands