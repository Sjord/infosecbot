from infosecbot.storage import storage
import tweepy
from infosecbot.webclient import webclient
from bs4 import BeautifulSoup
from infosecbot.model import Link

def get_tweepy_api():
    consumer_key = storage['twitter']['consumer_key']
    consumer_secret = storage['twitter']['consumer_secret']
    access_token = storage['twitter']['access_token']
    access_token_secret = storage['twitter']['access_token_secret']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

def retrieve_title(url):
    html = webclient.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    return soup.title.string

def gather_urls():
    api = get_tweepy_api()
    public_tweets = api.home_timeline()
    links = []
    for t in public_tweets:
        for url in [u['expanded_url'] for u in t.entities['urls']]:
            try:
                title = retrieve_title(url)
                links.append(Link({
                    "url": url,
                    "title": title,
                    # "by": t.user
                }))
            except Exception as e:
                print(e)
    return links


if __name__ == "__main__":
    print(get_links())
