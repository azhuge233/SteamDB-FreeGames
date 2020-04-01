import ssl, time
from bs4 import BeautifulSoup
from urllib import request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

HEAD = dict({})
HEAD['USER-AGENT'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/80.0.3987.149 Safari/537.36 Edg/80.0.361.69"
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


def selenium_get_url(url, delay=0, nopic=False):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    if nopic:
        prefs = {'profile.managed_default_content_settings.images': 2}
        chrome_options.add_experimental_option('prefs', prefs)

    browser = webdriver.Chrome(options=chrome_options)
    browser.get(url)
    time.sleep(delay)
    html = browser.page_source
    browser.close()

    return BeautifulSoup(html, 'lxml')
