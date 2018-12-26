from infosecbot.webclient import webclient
from infosecbot.model import Link, Source
import feedparser
from random import randrange

rss_feed = "https://www.sjoerdlangkemper.nl/feed.xml"


def gather_urls():
    if randrange(100) == 0:
        response = webclient.get(rss_feed)
        response.raise_for_status()
        feed = feedparser.parse(response.content)
        for item in feed.entries:
            link = Link(item.link, Source("sjoerdlangkemper", None))
            link.title = item.title
            link.description = item.description
            yield link


if __name__ == "__main__":
    u = gather_urls()
    for l in u:
        print(l)
