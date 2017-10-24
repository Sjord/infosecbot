from storage import storage
import tweepy

def get_tweepy_api():
    consumer_key = storage['twitter']['consumer_key']
    consumer_secret = storage['twitter']['consumer_secret']
    access_token = storage['twitter']['access_token']
    access_token_secret = storage['twitter']['access_token_secret']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

def get_links():
    api = get_tweepy_api()
    public_tweets = api.home_timeline()
    links = []
    for t in public_tweets:
        for url in [u['expanded_url'] for u in t.entities['urls']]:
            links.append({
                "url": url,
                # "by": t.user
            })
    return links


if __name__ == "__main__":
    print(get_links())
