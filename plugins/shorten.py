import requests

def shorten_url(bot, url):
    API_KEY = bot.SECRETS["other"]["noxd_shorten_key"]

    host = "https://noxd.co/"

    response = requests.post(host, data={'link':url,
        'api_key':API_KEY}).json()

    try:
        return host + response['Id']
    except Exception as e:
        return "Error: {0}".format(e)
