#!/usr/bin/env py3
from __future__ import division, print_function, absolute_import

import os
import sys
import re

'''
 ============================
 @FileName: GSearch
 @Author:   Jeff Pan (kevinjjp@gmail.com)
 @Version:  1.0 
 @DateTime: 2017-12-06 10:41:23
 ============================
'''
class GSearch:
    """docstring for GSearch"""
    def __init__(self, logger):
        self.logger =logger 
        self.url= '' 
        self.title = '' 
        self.snippet = '' 
        self.logger.info("GSearch Initialization Completed.")

    def get_URL(self):
        return self.url

    def set_URL(self, url):
        self.url = url 

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title

    def get_snippet(self):
        return self.snippet

    def set_snippet(self, content):
        self.snippet = content

    def display(self, prefix = ''):
        self.logger.info ('url\t->%s'%self.url)
        self.logger.info ('title\t->%s'% self.title.decode())
        try:
            self.logger.info ('content\t->%s'% self.snippet.decode())
        except:
            self.logger.info ('content\t->%s'% self.snippet)

    def writeFile(self, filename):
        with open(filename, 'a', encoding="utf-8") as file:
            try:
                file.write('url:%s\n'%self.url)
                file.write('tit:%s\n'%self.title.decode())
                file.write('spt:%s\n'%re.sub("\n", "", self.snippet.decode()))
            except:
                file.write('spt:%s\n'%re.sub("\n", "", self.snippet))