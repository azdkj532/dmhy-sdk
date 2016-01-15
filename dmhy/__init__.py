#!/usr/bin/env python3

import re

import requests
from bs4 import BeautifulSoup


def GetMagnetLink(url):
    try:
        res = requests.get(url)
    except:
        return None
    data = res.content.decode('utf-8')
    if res.status_code != 200:  # the http status
        print("network error: %d " % res.status_code)
        return None
    pattern = re.search(r"magnet:[^\"\s<>]*", data)
    if pattern:
        return pattern.group()
    else:
        return None


class dmhy():
    def __init__(self, title="", url=""):
        self._title = title
        self._url = url
        self._magnet = ""
        self.date = ""

    def __str__(self):
        return self._title

    def __rper__(self):
        return self._title

# parameter url must be an absolute path ( including http://... )
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        if not isinstance(title, str):
            raise TypeError("Excepted a string")
        self._title = title

    @property
    def magnet(self):
        if not self._magnet:
            self._magnet = self.GetMagnetLink(self._url)
        return self._magnet

    @magnet.setter
    def magnet(self, magnet):
        if not isinstance(magnet, str):
            raise TypeError("Excepted a string")
        self._magnet = magnet

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        if not isinstance(url, str):
            raise TypeError("Excepted a string")
        self._url = url

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        if isinstance(date, str):
            self._date = date
        else:
            raise TypeError("Excepted a string")

# get an parameter, keywords it can be a string or a list


def Search(keyword):

    if isinstance(keyword, str):
        # keywords should split by space(s)
        keyword_list = filter(None, keyword.split(' '))
    elif isinstance(keyword, (list, tuple)):
        if all([isinstance(_, str) for _ in keyword]):
            keyword_list = keyword
        else:
            raise TypeError("Excepted a string")
    else:
        raise TypeError("Expected a string or a list of string")
    keyword_list = [_ for _ in filter(None, keyword_list)]
    url = u"http://share.dmhy.org/topics/list?keyword={0}" \
          .format('+'.join(keyword_list))

    try:
        res = requests.get(url)
    except:
        raise StopIteration

    if res.status_code != 200:
        raise StopIteration

    html = res.content
    parser = BeautifulSoup(html.decode(), "html.parser")
    try:
        table = parser.find(id='topic_list').tbody.find_all('tr')
    except:
        raise StopIteration
    else:
        for topic in table:
            date = topic.find(style="display: none;").get_text()
            source = topic.find(target="_blank")
            while source.find('span') is not None:
                source.span.unwrap()
            title = source.get_text().strip()
            url = "http://share.dmhy.org"+source['href']
            magnet = topic.find(class_="download-arrow arrow-magnet")
            animation = dmhy(title=title, url=url)
            if magnet:
                animation.magnet = magnet['href']
            animation.date = date
            yield animation
