from infosecbot.webclient import webclient
from infosecbot.storage import storage
from infosecbot.model import Link, Source
from html import unescape
import feedparser
import re

arxiv_rss_feed = "http://export.arxiv.org/rss/cs.CR"


def gather_urls():
    response = webclient.get(arxiv_rss_feed)
    response.raise_for_status()
    feed = feedparser.parse(response.content)
    for item in feed.entries:
        m = re.match(r"^(.*)\. \(arXiv:(.*) \[cs.CR\]\)$", item.title)
        if m:
            title = m.group(1)
            id = m.group(2)
            link = Link(item.link, Source("arxiv", id))
            link.title = title
            link.description = item.description
            yield link


if __name__ == "__main__":
    u = gather_urls()
    print(u)
