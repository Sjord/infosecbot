import infosecbot.provider.reddit as reddit
import infosecbot.provider.hackernews as hackernews
import infosecbot.provider.twitter as twitter
import infosecbot.provider.rss as rss
from infosecbot.classifier import LinkClassifier
from infosecbot.storage import storage
from infosecbot.lockfile import LockFile
from infosecbot.timeout import Timeout
from random import randrange
import sys


class SeenIt:
    def __init__(self):
        self.seen_urls = set([l.url for l in storage["links"]])
        self.seen_titles = set([l.title for l in storage["links"]])

    def seen(self, link):
        seen = link.url in self.seen_urls or link.title in self.seen_titles
        self.seen_urls.add(link.url)
        self.seen_titles.add(link.title)
        return seen


def collect_links():
    providers = [reddit, hackernews, twitter, rss]
    seenit = SeenIt()

    for p in providers:
        links = p.gather_urls()
        for link in links:
            if not seenit.seen(link):
                yield (link)


def is_probably_infosec(link):
    return link.infosec_probability > 0.9


if __name__ == "__main__":
    with Timeout(1200):
        with LockFile():
            twitter.update_retweet_votes()
            classifier = LinkClassifier()
            new_links = []

            try:
                for l in collect_links():
                    l.infosec_probability = classifier.classify(l)
                    if is_probably_infosec(l):
                        storage["links"].append(l)
                        new_links.append(l)
            finally:
                storage.save()

            if "tweet" in sys.argv:
                twitter.handle_new_links(new_links)
