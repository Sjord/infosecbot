
from urllib.parse import urlparse
import hashlib


def hash_url(url):
    return hashlib.sha256(url.encode()).hexdigest()[0:16]


class Link:
    def __init__(self, data):
        self.title = data['title']
        self.url = data['url']

        try:
            self.id = data['id']
        except KeyError:
            self.id = hash_url(self.url)

        try:
            self.score = data['score']
        except KeyError:
            self.score = 0

        try:
            self.learned_at_score = data['learned_at_score']
        except KeyError:
            self.learned_at_score = None
        
        parsed_url = urlparse(self.url)
        self.domain = parsed_url.hostname
    
    def __str__(self):
        return "%s <%s>" % (self.title, self.url)
