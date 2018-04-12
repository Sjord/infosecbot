from infosecbot.webclient import webclient
from bs4 import BeautifulSoup

def parse_title(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.title.string.strip()

def retrieve_title(url):
    return parse_title(webclient.get(url).content)

class Webpage:
    pass

def retrieve(url):
    response = webclient.get(url)
    result = Webpage()
    result.title = parse_title(response.content)
    result.url = response.url
    return result
