#!/usr/bin/env python3

import re

import requests
from bs4 import BeautifulSoup

RE_MAGNET = re.compile(r'href="(magnet:.+)"')

__all__ = [ 'AnimateEntry', 'search', 'DMHYError', 'NetworkError' ]

class DMHYError(Exception):
    def __init__(self, description, source_error):
        super().__init__()
        self.description = description
        self.source_error = source_error

    def __repr__(self):
        return '%s(%r, %r)' % (
            self.__class__.__name__, self.description, self.source_error
        )

    def __str__(self):
        return repr(self)


class NetworkError(DMHYError):
    def __init__(self, description, source_error=None):
        super().__init__(description, source_error)

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
        except Exception as ex:
            raise NetworkError('failed to get url: %r' % self.url, ex)

        data = res.text
        if res.status_code != 200:  # the http status
            raise NetworkError('non-200 http status code (%d) for url %r' % (
                res.status_code, self.url
            ), None)

        result = RE_MAGNET.search(data)
        self._magnet_link = result and result.group(1)
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


def search(keywords):
    """
    returns a generator that yields AnimateEntry instance with your keywords

    :param:keywords: your keywords
    :type:keywords: str, list, tuple, or any iterable type
    """
    if hasattr(keywords, '__iter__'):
        keywords = ' '.join(keywords)
    else:
        keywords = str(keywords)

    try:
        res = requests.get("http://share.dmhy.org/topics/list", params={
            'keyword': keywords
        })
    except Exception as ex:
        raise NetworkError('failed to get search results', ex)

    if res.status_code != 200:
        raise NetworkError(
            'search results page returned non-200 http status (%d)' % (
                res.status_code
            ), ex
        )

    parser = BeautifulSoup(res.text, "html5lib")
    try:
        table = parser.find(id='topic_list').tbody.find_all('tr')
    except Exception as ex:
        raise DMHYError('can not extract search result', ex)

    for topic in table:
        date = topic.select('td span')[0].text
        source = topic.find('a', target="_blank")
        title = source.text.strip()
        url = "http://share.dmhy.org" + source['href']
        magnet_anchor = topic.find(class_="download-arrow arrow-magnet")
        yield AnimateEntry(
            title, url, date, magnet_anchor and magnet_anchor['href']
        )

def Search(keywords):
    import sys
    print('Warning: dmhy.Serach is deprecated, use dmhy.serach instead.',
            file=sys.stderr)
    for result in search(keywords):
        yield result
