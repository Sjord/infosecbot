import sys
from infosecbot.storage import storage
from infosecbot.model import Link, Source

if __name__ == "__main__":
    for url in sys.argv[1:]:
        try:
            link = storage.find_link_by_url(url)
            if link is None:
                source = Source("manual", None)
                link = Link.from_url(url, source)
                storage['links'].append(link)
                print("Created new link for " + str(link))
            link.score += 1
        except Exception as e:
            print("Failed to add '%s': %s" % (url, str(e)))
    storage.save()
