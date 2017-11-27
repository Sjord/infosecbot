from infosecbot.webclient import webclient
from infosecbot.storage import storage
from infosecbot.model import Link

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
    for id in ids:
        story = get_story(id)
        if 'url' in story:
            yield Link(story['url'], story['title'])


if __name__ == "__main__":
    for u in gather_urls():
        print(u)
    storage.save()
