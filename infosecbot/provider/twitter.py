from infosecbot.storage import storage
import tweepy
from infosecbot.model import Link
import random
from infosecbot.webpage import retrieve


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
                page = retrieve(url)
                links.append(Link(page.url, page.title))
            except Exception as e:
                print(e)
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
