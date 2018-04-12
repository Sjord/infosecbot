from infosecbot.webclient import webclient
from bs4 import BeautifulSoup

def retrieve_title(url):
    html = webclient.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    return soup.title.string.strip()


