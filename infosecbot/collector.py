import infosecbot.provider.reddit as reddit
import infosecbot.provider.hackernews as hackernews
from infosecbot.classifier import load_classifier
from infosecbot.storage import storage

def collect_links():
    providers = [reddit, hackernews]
    classifier = load_classifier()

    for p in providers:
        links = p.gather_urls()
        for link in links:
            is_infosec = classifier.classify(link.title)
            if is_infosec:
                yield link


if __name__ == "__main__":
    for l in collect_links():
        print(l)
        storage['urls'].append(l)
    
    storage.save()
