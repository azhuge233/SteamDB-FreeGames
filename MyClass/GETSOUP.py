import ssl, time
import undetected_chromedriver
from bs4 import BeautifulSoup
from urllib import request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from playwright import sync_playwright

HEAD = dict({})
HEAD['USER-AGENT'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/80.0.3987.149 Safari/537.36 Edg/80.0.361.69"
CONTEXT = ssl._create_unverified_context()

TYPE_LIST = ["chromium", "firefox", "webkit"]

GET_PAGE_SOURCE_ERROR_MSG = "Get page source error!"


def get_url_single(url, headers=None, decode='utf-8'):
    if headers is not None:
        HEAD.update(headers)
    req = request.Request(url, headers=HEAD)
    if "https" in url:
        response = request.urlopen(req, context=CONTEXT)
    else:
        response = request.urlopen(req)
    html = response.read().decode(decode)
    soup = BeautifulSoup(html, 'lxml')
    
    return soup


def get_url_list(url, headers=None, decode='utf-8'):
    if headers is not None:
        HEAD.update(headers)
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


def selenium_get_url(url, delay=0, nopic=False, uc=False):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    if nopic:
        prefs = {'profile.managed_default_content_settings.images': 2}
        chrome_options.add_experimental_option('prefs', prefs)
        
    if uc:
        browser = undetected_chromedriver.Chrome()
    else:
        browser = webdriver.Chrome(options=chrome_options)
        
    try:
        browser.get(url)
        if delay != 0:
            time.sleep(delay)
        html = browser.page_source
    except:
        print(GET_PAGE_SOURCE_ERROR_MSG)
        pass
    finally:
        browser.close()
        
    return BeautifulSoup(html, 'lxml')

def playright_get_url(url, type="firefox", delay=0, headless=True):
    type = type.lower()
    if type not in TYPE_LIST:
        raise Exception("Type {} is invalid.\nTYPE should only be 'chromium' 'firefox' or 'webkit'".format(type))
    
    with sync_playwright() as p:
        if type == TYPE_LIST[0]:
            browser = p.chromium.launch(headless=headless)
        elif type == TYPE_LIST[1]:
            browser = p.firefox.launch(headless=headless)
        else:
            browser = p.webkit.launch(headless=headless)
            
        try:
            page = browser.newPage()
            page.goto(url=url)
            if delay != 0:
                time.sleep(delay)
            html = page.innerHTML("*")
        except:
            raise Exception(GET_PAGE_SOURCE_ERROR_MSG)
        finally:
            browser.close()
        
        return BeautifulSoup(html, 'lxml')
