import ssl
from bs4 import BeautifulSoup
from urllib import request


class MyBS:
    url = ""
    selection = ""
    find_key = ""
    url_l = list([])
    head = dict({})

    def __init__(self):
        self.url = ""
        self.selection = ""
        self.find_key = ""
        self.head['USER-AGENT'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                                  "Chrome/75.0.3770.100 Safari/537.36"

    def add_header(self, name, content):
        self.head[name] = content
    
    def get_url_single(self, url_, decode='utf-8'):
        self.url = url_
        req = request.Request(self.url, headers=self.head)
        if "https" in url_:
            context = ssl._create_unverified_context()
            response = request.urlopen(req, context=context)
        else:
            response = request.urlopen(req)
        html = response.read().decode(decode)
        soup = BeautifulSoup(html, 'lxml')

        return soup

    def get_url_list(self, url_, decode='utf-8'):
        soup = list()
        if "https" in url_:
            context = ssl._create_unverified_context()
        self.url_l = url_
        for each in self.url_l:
            req = request.Request(each, headers=self.head)
            if "https" in url_:
                response = request.urlopen(req, context=context)
            else:
                response = request.urlopen(req)
            html = response.read().decode(decode)
            soup.append(BeautifulSoup(html, 'lxml'))

        return soup

    # def select(self, soup, selection_):
    #     self.selection = selection_
    #     return soup.select(self.selection)
    #
    # def find(self, soup, find_key_):
    #     self.find_key = find_key_
    #     return soup.find(self.find_key)
    #
    # def find_all(self, soup, find_key_):
    #     self.find_key = find_key_
    #     return soup.find_all(self.find_key)
