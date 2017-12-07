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
    def __init__(self, logger, google_mirror, results_num , lang, agent_list ):
        self.logger = logger
        self.results_num = results_num
        self.google_mirror = google_mirror
        self.agent_list = agent_list
        self.lang = lang

        self.user_agent = self.__get_agent_list()

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

    def __get_agent_list(self):
        agents = []
        self.logger.info("load agent list: %s"%self.agent_list)
        with open(self.agent_list, 'r', encoding='utf-8') as fi:
            for line in fi:
                line = line.strip()
                if line != "":
                    agents.append(line)
        return agents

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

    def search(self, query, show_dup = False):
        lang = self.lang
        num = self.results_num
        num_per_page = 10
        base_url = self.google_mirror
        search_results = []
        index_range = len(self.user_agent)
        query = urllib.request.quote(query)
        if(num % self.results_num == 0):
            pages = int(num / num_per_page)
        else:
            pages = int(num / num_per_page) + 1
        if show_dup:
            dup = 0
        else:
            dup = 1
        self.logger.info("Total Fectching: %d Pages/ %d Results "%(pages, num))
        for p in range(0, max(1, pages)):
            self.logger.info("Fectching %d/%d"%(p+1, pages))
            start = p * num_per_page
            url = 'https://%s/search?hl=%s&fitler=%d&num=%d&start=%s&q=%s' % (base_url, lang, dup, num_per_page, start, query)
            retry = 3
            while(retry > 0):
                try:
                    request = urllib.request.Request(url)
                    agent_index = random.randint(0, index_range - 1)
                    user_agent = self.user_agent[agent_index]
                    request.add_header('User-Agent', user_agent)
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
                    self.logger.error(e)
                    self.__gsleep()
                    retry = retry - 1
                    continue            
                except Exception as e:
                    self.logger.error ("error:%s"% e)
                    retry = retry - 1
                    self.__gsleep()
                    continue
            
        return search_results 
