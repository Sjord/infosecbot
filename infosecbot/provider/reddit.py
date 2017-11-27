from infosecbot.webclient import webclient
from infosecbot.storage import storage
from infosecbot.model import Link

default_reddits = ['crypto', 'netsec', 'hacking']
default_sort = 'new'


def get_links(id, reddits, sort):
    reddit_url = "https://www.reddit.com/r/%s/%s/.json" % ("+".join(reddits), sort)
    response = webclient.get(reddit_url)
    response.raise_for_status()
    return response.json()


def gather_urls(reddits=None, sort=None):
    reddits = reddits or default_reddits
    sort = sort or default_sort

    last_id = storage["reddit"]["last_id"]
    links = get_links(last_id, reddits, sort)
    children = [c['data'] for c in links['data']['children']]
    return [Link(c['url'], c['title']) for c in children if not c['is_self']]


if __name__ == "__main__":
    u = gather_urls()
    print(u)
    print(len(u))
    storage.save()
