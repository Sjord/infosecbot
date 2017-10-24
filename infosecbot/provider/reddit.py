from webclient import webclient
from storage import storage

reddit_url = "https://www.reddit.com/r/crypto+netsec+hacking/new/.json"


def get_links(id):
    response = webclient.get(reddit_url)
    response.raise_for_status()
    return response.json()


def gather_urls():
    last_id = storage["reddit"]["last_id"]
    links = get_links(last_id)
    children = [c['data'] for c in links['data']['children']]
    return [c for c in children if not c['is_self']]


if __name__ == "__main__":
    u = gather_urls()
    print(u)
    print(len(u))
    storage.save()
