from infosecbot.webclient import webclient
from bs4 import BeautifulSoup
import re

def parse_title(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.get_text(strip=True)
    title = re.sub(r"\s+", " ", title)
    return title

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
