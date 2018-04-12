import infosecbot.provider.reddit as reddit
import infosecbot.provider.hackernews as hackernews
import infosecbot.provider.twitter as twitter
from infosecbot.classifier import load_classifier
from infosecbot.storage import storage


class SeenIt:
    def __init__(self):
        self.seen_urls = set([l.url for l in storage['links']])

    def seen(self, url):
        seen = url in self.seen_urls
        self.seen_urls.add(url)
        return seen


def collect_links():
    providers = [reddit, hackernews, twitter]
    classifier = load_classifier()
    seenit = SeenIt()

    for p in providers:
        links = p.gather_urls()
        for link in links:
            if not seenit.seen(link.url):
                is_infosec = classifier.classify(link)
                if is_infosec:
                    yield link


if __name__ == "__main__":
    new_links = []

    for l in collect_links():
        print(l)
        new_links.append(l)
        storage['links'].append(l)
    
    storage.save()
    twitter.handle_new_links(new_links)
