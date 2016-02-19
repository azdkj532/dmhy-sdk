#!/usr/bin/env python3

import re

import requests
from bs4 import BeautifulSoup

RE_MAGNET = re.compile(r'href="(magnet:.+)"')

__all__ = [ 'AnimateEntry', 'Search']

class AnimateEntry(object):
    def __init__(self, title, url, date, magnet_link=None):
        self.title = title
        self.url = url
        self.date = date
        self._magnet_link = magnet_link

    def get_magnet_link(self):
        if self._magnet_link:
            return self._magnet_link

        try:
            res = requests.get(self.url)
        except:
            print('Can not get (%r)' % self.url)
            return None

        data = res.text
        if res.status_code != 200:  # the http status
            print("http status: %d, url = %s" % (
                res.status_code, self.url
            ))
            return None

        result = RE_MAGNET.search(data)
        try:
            self._magnet_link = result.group(1)
        except:
            print('Can not find magnet')
            return None
        return self._magnet_link

    @property
    def magnet(self):
        """
        return magnet link, for backward compatibility
        """
        return self.get_magnet_link()

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return '%s(title=%r, url=%r, date=%r)' % (
            self.__class__.__name__,
            self.title, self.url, self.date
        )

# get an parameter, keywords it can be a string or a list


def Search(keyword):
    """
    returns a generator that yields AnimateEntry instance with your keywords

    :param:keyword: your keywords
    :type:keyword: str, list, tuple
    """
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
            magnet_anchor = topic.find(class_="download-arrow arrow-magnet")
            animation = AnimateEntry(
                title, url, date, magnet_anchor and magnet_anchor['href']
            )
            yield animation
