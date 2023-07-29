import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from cfg import config, db_cfg


def is_valid(url):
    '''
    This function checks if a url is valid or not
    '''
    parsed = urlparse(url)
    return bool(parsed.netloc) and ((parsed.scheme)=='http' or (parsed.scheme)=='https' )


def get_all_links(url):
    '''
    :return: set of all unique urls on the current url
    '''
    new_urls = set()
    try:
        soup = BeautifulSoup(requests.get(url, verify=False).content, "html.parser")
    except requests.exceptions.SSLError:
        return new_urls
    for a_tags in soup.findAll("a"):
        href = a_tags.attrs.get("href")
        if href=="" or href==None:
            continue
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        href = parsed_href.scheme+"://"+parsed_href.netloc+parsed_href.path
        if not is_valid(href):
            continue
        if href in url:
            continue
        new_urls.add(href)
    return new_urls    

