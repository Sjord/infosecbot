
from urllib.parse import urlparse

class Link:
    def __init__(self, data):
        self.title = data['title']
        self.url = data['url']
        
        parsed_url = urlparse(self.url)
        self.domain = parsed_url.hostname
    
    def __str__(self):
        return "%s <%s>" % (self.title, self.url)
