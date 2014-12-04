#!/usr/bin/env python3

import re

import urllib3
from bs4 import BeautifulSoup

#get an parameter, keywords it can be a string or a list
def Search( keywords ):

    if type(keywords) in (unicode, str):
        #keywords should split by space(s)
        url = u"http://share.dmhy.org/topics/list?keyword={keyword}".format( keyword= '+'.join(filter( None ,keywords.split(' '))))
    elif type(keywords) is list:
        url = u"http://share.dmhy.org/topics/list?keyword={keyword}".format( keyword='+'.join(filter( None,keywords) ))
    else:
        return []

    page = urllib3.PoolManager()
    res = page.request( 'GET', url )
    if res.status != 200 :
        return []

    parser = BeautifulSoup( res.data )
    try:
        table = parser.find( id='topic_list').tbody.find_all('tr')
    except: return []
    else:
        download_list = []
        for topic in table:
            date = topic.find(style="display: none;").get_text().encode("utf-8")
            source = topic.find( target="_blank" )
            while source.find('span') != None :
                source.span.unwrap()
            title = re.findall( r"\S+.*", source.get_text() )
            if len(title) > 0: 
                title = title[0] #the first result that reg had matched is what we want
            else: 
                continue #if reg didn't match anything, pass this topic
            download_list.append({ 'title':title, 'url':source['href'], 'date':date })
        return download_list

#parameter url must be an absolute path ( including http://... )
def GetMagnetLink( url ):
    page = urllib3.PoolManager()
    try:
        res = page.request( 'GET', url.encode('utf-8') )
    except:
        return None
    else:
         #the http status
         if res.status != 200:
             return None
         magnet = re.findall( r"magnet:[^\"\s<>]*", res.data )
         if len(magnet) != 0:
             return magnet[0]
         else:
             return None
