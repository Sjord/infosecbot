from infosecbot.webclient import webclient
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
from datetime import date
import dateparser

class Webpage:
    def __str__(self):
        return str(self.__dict__)

def parse_title_from_meta(soup):
    meta = soup.select_one("meta[property='og:title']") \
        or soup.select_one("meta[name='twitter:title']")
    if meta is None:
        return None
    return meta.attrs.get("content")

def parse_title_from_tag(soup):
    title = soup.title.get_text(strip=True)
    title = re.sub(r"\s+", " ", title)
    return title

def parse_title(soup):
    return parse_title_from_meta(soup) or parse_title_from_tag(soup)

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


def parse_date_str(soup):
    meta = soup.select_one("meta[property='article:published_time']") \
        or soup.select_one("meta[property='article:modified_time']") \
        or soup.select_one("meta[itemprop='datePublished']") \
        or soup.select_one("meta[itemprop='dateModified']")
    
    if meta is not None:
        return meta.attrs.get("content")

    time = soup.select_one("time[datetime]")
    if time is not None:
        return time.attrs.get("datetime")

    return None


def guess_year(url):
    year = date.today().year
    for i in range(10):
        if str(year) in url:
            return year
        year -= 1
    return None


def search_url_date(url):
    matches = re.findall(r'20[0-9/-]+', url)
    return max(matches, default=None)


def search_html_date(html):
    m = re.search(b"(20[0123]\d-[01]\d-[0123]\d)(T|\b)", html)
    if m:
        return m.group(1).decode()
    return None


def parse_date(url, html, soup):
    date_str = parse_date_str(soup)
    if date_str:
        return dateparser.parse(date_str)

    date_str = search_html_date(html)
    if date_str:
        return dateparser.parse(date_str)

    date_str = search_url_date(url)
    if date_str:
        return dateparser.parse(date_str)

    return None


def retrieve(url):
    response = webclient.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    result = Webpage()
    result.title = parse_title(soup)
    result.description = parse_description(soup)
    result.date = parse_date(url, response.content, soup)
    result.url = urljoin(response.url, parse_canonical(soup))
    return result


if __name__ == "__main__":
    print(retrieve("https://jakearchibald.com/2018/i-discovered-a-browser-bug/"))
    print(retrieve("https://www.sjoerdlangkemper.nl/2018/06/20/discovering-subdomains/"))
    print(retrieve("https://developer.twitter.com/en/docs/tweets/optimize-with-cards/overview/summary.html"))
