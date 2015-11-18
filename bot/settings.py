import configparser

def get_config():
    #Uses configparser to load the config file
    dict1 = {}
    Config = configparser.ConfigParser()
    Config.read("config.ini")
    options = Config.options("Settings")
    for option in options:
        if option != "startchannels":
            dict1[option] = Config.get("Settings", option)
        else:
            dict1[option] = []
            for channel in Config.get("Settings", option).split(','):
                dict1[option].append("#{0}".format(channel))
    return dict1