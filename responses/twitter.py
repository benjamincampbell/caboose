from bot.response import response

@response("twitter.com")
def twitter(bot, line):
    pass
    # import logging
    # import requests
    # import tweepy
    # from bot.colors import color
    # from plugins.shorten import shorten_url

    # tweet_id_match = line.link_match.group(4)

    # try:
    #     if "status" in tweet_id_match:
    #         bearer_token = bot.SECRETS["other"]["twitter_bearer_token"]
    #         consumer_key = bot.SECRETS["api_keys"]["twitter"]
    #         consumer_secret = bot.SECRETS["other"]["twitter_secret"]
    #         access_token = bot.SECRETS["other"]["twitter_access_token"]
    #         access_token_secret = bot.SECRETS["other"]["twitter_access_token_secret"]


    #         client = tweepy.Client(
    #             bearer_token=bearer_token,
    #             consumer_key=consumer_key,
    #             consumer_secret=consumer_secret,
    #             access_token=access_token,
    #             access_token_secret=access_token_secret)

            
    #         tweet_id = tweet_id_match.split("/")[3].split("?")[0]

    #         tweet = client.get_tweet(tweet_id)

    #         line.reply("yes there is a {twitter} link somewhere in that line".format(twitter=color("twitter", "lightcyan")))
    # except Exception as e:
    #     print(e)