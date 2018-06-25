
from urllib.parse import urlparse
import hashlib
from datetime import datetime, timezone
from infosecbot.webpage import retrieve
from infosecbot.wordfile import load_words


def hash_url(url):
    return hashlib.sha256(url.encode()).hexdigest()[0:16]


class Source:
    def __init__(self, source, id):
        self.source = source
        self.id = id

    def serialize(self):
        return self.__dict__


class Blacklist:
    def __init__(self):
        self.prefixes = load_words("urlblacklist.txt")

    def contains(self, url):
        for prefix in self.prefixes:
            if url.startswith(prefix):
                return True
        return False


blacklist = Blacklist()


class Link:
    def __init__(self, url, source):
        if not url:
            raise ValueError("empty url")

        self.url = url
        self.source = source
        self.id = hash_url(url)
        self.score = 0
        self.learned_at_score = None
        self.created = datetime.now(timezone.utc)

        parsed_url = urlparse(self.url)
        self.domain = parsed_url.hostname
        self.scheme = parsed_url.scheme

        if self.domain is None:
            raise ValueError("invalid url")

    @classmethod
    def from_url(cls, url, source):
        if url.endswith(".pdf"):
            raise ValueError("PDF")

        if blacklist.contains(url):
            raise ValueError("url is blacklisted")

        webpage = retrieve(url)

        if blacklist.contains(webpage.url):
            raise ValueError("url is blacklisted")

        self = cls(webpage.url, source)
        self.title = webpage.title
        self.description = webpage.description
        return self

    @classmethod
    def unserialize(cls, data):
        self = cls(data['url'], data['source'])
        self.title = data['title']
        self.id = data['id']
        self.score = data['score']
        self.learned_at_score = data['learned_at_score']
        self.domain = data['domain']
        self.created = data.get('created')
        self.description = data.get('description')
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
