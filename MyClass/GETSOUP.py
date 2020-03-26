import ssl
from bs4 import BeautifulSoup
from urllib import request

HEAD = dict({})
HEAD['USER-AGENT'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                        "Chrome/75.0.3770.100 Safari/537.36"
CONTEXT = ssl._create_unverified_context()


def get_url_single(url, decode='utf-8'):
    req = request.Request(url, headers=HEAD)
    if "https" in url:
        response = request.urlopen(req, context=CONTEXT)
    else:
        response = request.urlopen(req)
    html = response.read().decode(decode)
    soup = BeautifulSoup(html, 'lxml')
    
    return soup


def get_url_list(url, decode='utf-8'):
    soup = list([])
    
    for each in url:
        req = request.Request(each, headers=HEAD)
        if "https" in url:
            response = request.urlopen(req, context=CONTEXT)
        else:
            response = request.urlopen(req)
        html = response.read().decode(decode)
        soup.append(BeautifulSoup(html, 'lxml'))
    
    return soup
