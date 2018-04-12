import sys
from infosecbot.webpage import retrieve_title
from infosecbot.storage import storage
from infosecbot.model import Link

if __name__ == "__main__":
    for url in sys.argv[1:]:
        link = storage.find_link_by_url(url)
        if link is None:
            title = retrieve_title(url)
            link = Link(url, title)
            storage['links'].append(link)
            print("Created new link for " + str(link))
        link.score += 1
    storage.save()
