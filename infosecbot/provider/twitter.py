from infosecbot.storage import storage
import tweepy
from infosecbot.model import Link, Source
import random
from infosecbot.webpage import retrieve


def is_twitter_url(url):
    return url.startswith("https://twitter.com/") or url.startswith("https://mobile.twitter.com/")


def get_tweepy_api():
    consumer_key = storage['twitter']['consumer_key']
    consumer_secret = storage['twitter']['consumer_secret']
    access_token = storage['twitter']['access_token']
    access_token_secret = storage['twitter']['access_token_secret']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

def gather_urls():
    api = get_tweepy_api()
    public_tweets = api.home_timeline(tweet_mode="extended")
    links = []
    for t in public_tweets:
        for url in [u['expanded_url'] for u in t.entities['urls']]:
            try:
                link = Link.from_url(url, Source("twitter", t.id))
                if not is_twitter_url(link.url):
                    links.append(link)
            except Exception as e:
                print(url, e)
    return links

def handle_new_links(links):
    if not links:
        return

    link = max(links, key = lambda l: l.infosec_probability)
    api = get_tweepy_api()
    api.update_status(str(link))


if __name__ == "__main__":
    for u in gather_urls():
        print(u)
