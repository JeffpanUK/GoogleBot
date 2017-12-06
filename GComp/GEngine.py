#!/usr/bin/env py3
from __future__ import division, print_function, absolute_import

import os
import sys
import re
import io
import time
import socket
import gzip
import random
import urllib
from urllib import error, request
from bs4 import BeautifulSoup 

from . import GSearch
# import pdb
'''
 ============================
 @FileName: GEngine
 @Author:   Jeff Pan (kevinjjp@gmail.com)
 @Version:  1.0 
 @DateTime: 2017-12-04 09:47:25
 ============================
'''

class GEngine:
    """docstring for GEngine"""
    def __init__(self, logger, google_mirror, results_num , lang ):
        self.logger = logger
        self.results_num = results_num
        self.google_mirror = google_mirror
        self.lang = lang

        self.user_agent = "Safari/533.4"
        self.logger.info("Set default user agent: %s"%self.user_agent)

        timeout = 40
        socket.setdefaulttimeout(timeout)
        self.logger.info("GEngine Initialization Completed.")


    def __gsleep(self):
        time.sleep(random.randint(60, 120))

    def __get_url(self, href):
        url = ''
        pattern = re.compile(r'(http[s]?://[^&]+)&', re.U | re.M)
        url_match = pattern.search(href)
        if(url_match and url_match.lastindex > 0):
            url = url_match.group(1)
        return url 

    def __get_search_results(self, html):
        results = []
        soup = BeautifulSoup(html, 'html.parser')
        div = soup.find('div', id='center_col')
        
        if div is not None:
            top = div.findAll('div', {'class': 'g'})
            if len(top) > 0:
                for li in top:
                    result = GSearch.GSearch(self.logger)
                    h3 = li.find('h3', {'class': 'r'})
                    if h3 == None:
                        continue

                    link = h3.find('a')
                    if link == None:
                        continue

                    url = link['href']
                    url = self.__get_url(url)
                    if url=='':
                        continue
                    title = link.renderContents()
                    result.set_URL(url)
                    result.set_title(title)

                    span = li.find('span', {'class': 'st'})
                    if (span!= None):
                        content = span.renderContents()
                        result.set_snippet(content)
                    results.append(result)
        return results

    def search(self, query):
        lang = self.lang
        num = self.results_num
        base_url = self.google_mirror
        search_results = []
        query = urllib.request.quote(query)
        if(num % self.results_num == 0):
            pages = int(num / self.results_num)
        else:
            pages = int(num / self.results_num) + 1

        for p in range(0, pages):
            start = p * num
            url = 'https://%s/search?hl=%s&num=%d&start=%s&q=%s' % (base_url, lang, num, start, query)
            retry = 3
            while(retry > 0):
                try:
                    request = urllib.request.Request(url)
                    user_agent = self.user_agent
                    request.add_header('User-agent', user_agent)
                    request.add_header('connection','keep-alive')
                    request.add_header('Accept-Encoding', 'gzip')
                    request.add_header('referer', base_url)
                    response = urllib.request.urlopen(request)
                    html = response.read()
                    
                    if(response.headers.get('content-encoding', None) == 'gzip'):
                        html = gzip.GzipFile(fileobj=io.BytesIO(html)).read()

                    results = self.__get_search_results(html)
                    search_results.extend(results)
                    break;
                except urllib.error.URLError as e:
                    print ('url error:'+ e)
                    self.__gsleep()
                    retry = retry - 1
                    continue            
                except Exception as e:
                    self.logger.error ("error:%s"% e)
                    retry = retry - 1
                    self.__gsleep()
                    continue
        return search_results 
