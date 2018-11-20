import infosecbot.provider.reddit as reddit
import infosecbot.provider.hackernews as hackernews
import infosecbot.provider.twitter as twitter
import infosecbot.provider.arxiv as arxiv
from infosecbot.classifier import LinkClassifier
from infosecbot.storage import storage
from infosecbot.lockfile import LockFile
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
    providers = [reddit, hackernews, twitter, arxiv]
    seenit = SeenIt()

    for p in providers:
        links = p.gather_urls()
        for link in links:
            if not seenit.seen(link):
                yield (link)


def autovote(link):
    prob = link.infosec_probability
    assert prob

    if prob > 0.999:
        link.score += 1
        return True

    if prob < 0.001 and randrange(100) == 0:
        link.score -= 1
        return True

    return False


def is_probably_infosec(link):
    return link.infosec_probability > 0.9


if __name__ == "__main__":
    with LockFile():
        new_links = []
        classifier = LinkClassifier()

        try:
            for l in collect_links():
                l.infosec_probability = classifier.classify(l)
                voted = autovote(l)
                if voted or is_probably_infosec(l):
                    storage["links"].append(l)
                    if is_probably_infosec(l):
                        new_links.append(l)
        finally:
            storage.save()

        if "tweet" in sys.argv:
            twitter.handle_new_links(new_links)
