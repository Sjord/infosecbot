
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
    date_fields = ['created', 'published']

    def __init__(self, url, source):
        if not url:
            raise ValueError("empty url")

        self.url = url
        self.source = source
        self.id = hash_url(url)
        self.score = 0
        self.learned_at_score = None
        self.created = datetime.now(timezone.utc)
        self.published = None

        parsed_url = urlparse(self.url)
        self.domain = parsed_url.hostname
        self.scheme = parsed_url.scheme

        if self.domain is None:
            raise ValueError("invalid url: '%s'" % self.url)

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
        self.published = webpage.date
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
        self.published = data.get('published')
        self.description = data.get('description')

        source_dict = data.get('source')
        if source_dict is not None:
            self.source = Source(source_dict['source'], source_dict['id'])

        for field_name in self.date_fields:
            if getattr(self, field_name) is not None:
                setattr(self, field_name, datetime.fromtimestamp(getattr(self, field_name), timezone.utc))
        return self

    def serialize(self):
        result = self.__dict__.copy()
        for field_name in self.date_fields:
            if result[field_name] is not None:
                result[field_name] = result[field_name].timestamp()
        return result
    
    def __str__(self):
        return "%s %s" % (self.title, self.url)

    def is_recent(self):
        return self.published is None or self.published.year == datetime.today().year
