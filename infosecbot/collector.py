import infosecbot.provider.reddit as reddit
import infosecbot.provider.hackernews as hackernews
import infosecbot.provider.twitter as twitter
from infosecbot.classifier import load_classifier
from infosecbot.storage import storage
import sys
import re


class SeenIt:
    def __init__(self):
        self.seen_urls = set([self.canonicalize(l.url) for l in storage['links']])
        self.seen_titles = set([l.title for l in storage['links']])

    def seen(self, link):
        canon_url = self.canonicalize(link.url)
        seen = canon_url in self.seen_urls or link.title in self.seen_titles
        self.seen_urls.add(canon_url)
        self.seen_titles.add(link.title)
        return seen

    def canonicalize(self, url):
        url = re.sub(r"[&?]utm_.*", "", url)
        url = re.sub(r"[&?/]$", "", url)
        return url


def collect_links():
    providers = [reddit, hackernews, twitter]
    classifier = load_classifier()
    seenit = SeenIt()

    for p in providers:
        links = p.gather_urls()
        for link in links:
            if not seenit.seen(link):
                prob = classifier.classify(link)
                link.infosec_probability = prob

                # Autovote
                if prob > 0.999:
                    link.score += 1

                # We consider high scores as infosec posts
                if prob > 0.9:
                    yield link


if __name__ == "__main__":
    new_links = []

    for l in collect_links():
        print(l)
        new_links.append(l)
        storage['links'].append(l)
    
    storage.save()

    if "tweet" in sys.argv:
        twitter.handle_new_links(new_links)
