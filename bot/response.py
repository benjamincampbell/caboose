import glob
import os
import logging

class resp(object):
    # basic response object

    def __init__(self, func, opts):
        self.func = func
        self.opts = opts
        self.enabled = True

    def __call__(self, *argv):
        return self.func(*argv)
    
    def __getattr__(self, name):
        return self.opts[name]
    
    def toggle_enabled(self):
        self.enabled = not self.enabled
        return self.enabled
    
def response(hostname, **options):
    """ Response format example:
    @response("twitter.com")
    def twitter(bot, line):
        line.conn.privmsg(line.args[0], line.text)
    """

    def decorator(function):
        global responses
        responses[hostname] = resp(function, options)
        return function
    return decorator
    
def reload_responses():
    #Loads all *.py files in responses/ into resp objects in the global responses dictionary
    logger = logging.getLogger("log")
    logger.info("Reloading responses")
    global responses
    responses = {}
    response_files = glob.glob(os.path.join("responses", "*.py"))
    for source in response_files:
        logging.info("Loading {0}".format(source))
        with open(source, 'r') as f:
            exec(compile(f.read(), source, "exec"))
    return responses