
from urllib.parse import urlparse
import hashlib


def hash_url(url):
    return hashlib.sha256(url.encode()).hexdigest()[0:16]


class Link:
    def __init__(self, url, title):
        self.title = title
        self.url = url
        self.id = hash_url(url)
        self.score = 0
        self.learned_at_score = None

        parsed_url = urlparse(self.url)
        self.domain = parsed_url.hostname


    @classmethod
    def unserialize(cls, data):
        self = cls(data['url'], data['title'])
        self.id = data['id']
        self.score = data['score']
        self.learned_at_score = data['learned_at_score']
        self.domain = data['domain']
        return self
    
    def __str__(self):
        return "%s <%s>" % (self.title, self.url)
