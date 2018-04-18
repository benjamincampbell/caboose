import requests

def shorten_url(bot, url):
    API_KEY = bot.SECRETS["other"]["worf_shorten_key"]

    response = requests.post("http://worf.co", data={'text':url,
        'shorten_key':API_KEY})

    try:
        return response.text
    except Exception as e:
        return "Error: {0}".format(e)
