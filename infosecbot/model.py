
from urllib.parse import urlparse
import hashlib
from datetime import datetime, timezone


def hash_url(url):
    return hashlib.sha256(url.encode()).hexdigest()[0:16]


class Link:
    def __init__(self, url, title):
        if not url:
            raise ValueError("url")

        if not title:
            raise ValueError("title")

        self.title = title
        self.url = url
        self.id = hash_url(url)
        self.score = 0
        self.learned_at_score = None
        self.created = datetime.now(timezone.utc)

        parsed_url = urlparse(self.url)
        self.domain = parsed_url.hostname


    @classmethod
    def unserialize(cls, data):
        self = cls(data['url'], data['title'])
        self.id = data['id']
        self.score = data['score']
        self.learned_at_score = data['learned_at_score']
        self.domain = data['domain']
        self.created = data.get('created')
        if self.created is not None:
            self.created = datetime.fromtimestamp(self.created, timezone.utc)
        return self

    def serialize(self):
        result = self.__dict__
        if result['created'] is not None:
            result['created'] = result['created'].timestamp()
        return result
    
    def __str__(self):
        return "%s %s" % (self.title, self.url)
