
from urllib.parse import urlparse

class Link:
    def __init__(self, data):
        self.title = data['title']
        self.url = data['url']

        try:
            self.id = data['id']
        except KeyError:
            import hashlib
            self.id = hashlib.sha256(self.url.encode()).hexdigest()[0:16]

        try:
            self.score = data['score']
        except KeyError:
            self.score = 0
        
        parsed_url = urlparse(self.url)
        self.domain = parsed_url.hostname
    
    def __str__(self):
        return "%s <%s>" % (self.title, self.url)
