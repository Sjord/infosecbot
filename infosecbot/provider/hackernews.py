from webclient import webclient
from storage import storage

newstories_url = 'https://hacker-news.firebaseio.com/v0/newstories.json'
item_url = 'https://hacker-news.firebaseio.com/v0/item/%d.json'


def newstories_ids(last_id):
    response = webclient.get(newstories_url)
    response.raise_for_status()
    return [id for id in response.json() if id > last_id]


def get_story(id):
    response = webclient.get(item_url % id)
    response.raise_for_status()
    return response.json()


def gather_urls():
    last_id = storage["hackernews"]["last_id"]
    ids = newstories_ids(last_id)
    if ids:
        storage["hackernews"]["last_id"] = max(ids)
    return (get_story(id) for id in ids)


if __name__ == "__main__":
    for u in gather_urls():
        print(u)
    storage.save()
