from infosecbot.webclient import webclient
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

class Webpage:
    def __str__(self):
        return str(self.__dict__)

def parse_title(soup):
    title = soup.title.get_text(strip=True)
    title = re.sub(r"\s+", " ", title)
    return title

def parse_canonical(soup):
    canonical_tag = soup.select_one("link[rel='canonical']")
    if canonical_tag is None:
        return None
    return canonical_tag.attrs.get("href")

def parse_description(soup):
    meta = soup.select_one("meta[name='description']") \
        or soup.select_one("meta[property='og:description']") \
        or soup.select_one("meta[name='twitter:description']")
    if meta is None:
        return None
    return meta.attrs.get("content")

def retrieve(url):
    response = webclient.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    result = Webpage()
    result.title = parse_title(soup)
    result.description = parse_description(soup)
    result.url = urljoin(response.url, parse_canonical(soup))
    return result


if __name__ == "__main__":
    print(retrieve("https://jakearchibald.com/2018/i-discovered-a-browser-bug/"))
    print(retrieve("https://www.sjoerdlangkemper.nl/2018/06/20/discovering-subdomains/"))
    print(retrieve("https://developer.twitter.com/en/docs/tweets/optimize-with-cards/overview/summary.html"))
