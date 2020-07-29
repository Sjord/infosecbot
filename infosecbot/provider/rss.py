from infosecbot.webclient import webclient
from infosecbot.model import Link, Source
import feedparser
from random import randrange
from urllib.parse import urljoin


def read_rss_feeds():
    with open("feeds.txt") as fp:
        for line in fp:
            yield line.strip()


def gather_urls(always=False):
    if always or randrange(100) == 0:
        for rss_feed in read_rss_feeds():
            response = webclient.get(rss_feed)
            response.raise_for_status()
            feed = feedparser.parse(response.content)
            for item in feed.entries:
                url = urljoin(rss_feed, item.link)
                link = Link(url, Source("rss", None))
                link.title = item.title
                link.description = item.description
                yield link


if __name__ == "__main__":
    u = gather_urls(always=True)
    for l in u:
        print(l)
