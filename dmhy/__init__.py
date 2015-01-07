#!/usr/bin/env python3

import re
from urllib.request import urlopen
from urllib.parse   import quote

from bs4 import BeautifulSoup

class dmhy():
    def __init__( self, title="", url="" ):
        self._title = title
        self._url = url
        self._magnet = ""
    def __str__( self ):
        return self._title
    def __rper__( self ):
        return self._title

    #parameter url must be an absolute path ( including http://... )
    @staticmethod
    def _GetMagnetLink( url ):
        try:
            res = urlopen( url )
        except:
            return None
             #the http status
        data = res.read().decode('utf-8')
        if res.status != 200:
            print( "network error: %d " % res.status )
            return None
        pattern = re.search( r"magnet:[^\"\s<>]*", data )
        if pattern:
            return pattern.group()
        else:
            return None

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
            self._magnet = self._GetMagnetLink(self._url)
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

#get an parameter, keywords it can be a string or a list
def Search( keyword ):

    if isinstance( keyword, str):
        #keywords should split by space(s)
        keywords = filter( None ,keyword.split(' '))
    elif isinstance( keyword, (list, tuple )):
        if all([ isinstance(_,str) for _ in keyword ]):
            keywords = keyword
        else:
            raise TypeError("Excepted a string")
    else:
        raise TypeError("Expected a string or a list of string") 
    keywords = [ quote(_) for _ in filter( None, keywords )]
    url = u"http://share.dmhy.org/topics/list?keyword={keyword}".format( keyword='+'.join(keywords) ) 
    
    try:
        res = urlopen(url)
    except:
        raise StopIteration

    if res.status != 200 :
        raise StopIteration

    parser = BeautifulSoup( res.read() )
    try:
        table = parser.find( id='topic_list').tbody.find_all('tr')
    except: 
        raise StopIteration
    else:
        for topic in table:
            #date = topic.find(style="display: none;").get_text()
            source = topic.find( target="_blank" )
            while source.find('span') is not None :
                source.span.unwrap()
            title = source.get_text().strip()
            url   = "http://share.dmhy.org"+source['href']
            yield dmhy( title=title, url=url )

