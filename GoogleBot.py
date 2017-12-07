#!/usr/bin/python  
#-*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import os
import sys
import re
import time

from GComp import GEngine

class GoogleBot(object):
    """docstring for GoogleBot"""
    def __init__(self, options, logger):
        os.system("chcp 65001")
        self.options = options
        self.logger = logger
        self.show_dup = options['show_dup']
        self.logger.info("GoogleBot Initialization Completed.")

    def process(self):
        # set expect search results number and searching language
        expect_num = self.options['number']
        lang = self.options['lang']
        google_mirror = self.options['google']
        agent_list = self.options['agent']
        # Create a GoogleAPI instance
        googleEngine = GEngine.GEngine(self.logger, google_mirror, expect_num, lang, agent_list)
        # if no parameters, read query keywords from file
        with open(self.options['target'], 'r', encoding='utf-8') as fi:
            for line in fi:
                keyword = line.strip()
                results = googleEngine.search(keyword, show_dup =self.show_dup)
                if self.show_dup:
                  self.logger.info("Totally %d results are shown, similar results are included."%(len(results)))
                  self.logger.info("If you want to only show the most relevant results, add the options '-d 0' or just remove the -d option")
                else:
                  self.logger.info("In order to show you the most relevant results, we have omitted some entries very similar to the %d already displayed." % (len(results)))
                  self.logger.info("If you like, you can repeat the search with the option '-d 1' to enable showing all results.")
                for r in results:
                    # r.display()
                    r.writeFile(self.options['results'])
                self.logger.info("Searching results has been saved in file %s"%self.options['results'])


if __name__ == '__main__':
  import time
  import logging
  from argparse import ArgumentParser

  parser = ArgumentParser(description='GoogleBot')
  parser.add_argument("--version", action="version", version="GoogleBot 1.0")
  parser.add_argument("-g", "--google", action="store", dest="google", default="www.google.com.tw", help='default google mirror')
  parser.add_argument("-n", "--num", action="store", dest="number", type=int ,default=20, help='results for each search')
  parser.add_argument("-l", "--lang", action="store", dest="lang", default='en', help='language for each search')
  parser.add_argument("-a", "--agent", action="store", dest="agent", default=r'agent.list', help='agent list to obey Google Rules')
  parser.add_argument("-d", "--dup", action="store", dest="show_dup", type = int, default=0, help='Whether show duplicated results')
  parser.add_argument("-r", "--results", action="store", dest="results", type = int, default='results.txt', help='searching results')
  parser.add_argument(type=str, action="store", dest="target", default="", help='company name list')

  args = parser.parse_args()
  options = vars(args)

  logger = logging.getLogger()
  formatter = logging.Formatter('[%(asctime)s][*%(levelname)s*][%(filename)s:%(lineno)d|%(funcName)s] - %(message)s', '%Y%m%d-%H:%M:%S')
  file_handler = logging.FileHandler('LOG-googleBot.txt', 'w','utf-8')
  file_handler.setFormatter(formatter)
  logger.addHandler(file_handler)

  stream_handler = logging.StreamHandler()
  stream_handler.setFormatter(formatter)
  logger.addHandler(stream_handler)
  logger.setLevel(logging.INFO)

  allStartTP = time.time()
  appInst = GoogleBot(options, logger)
  appInst.process()
  allEndTP = time.time()
  logger.info("Operation Finished [Time Cost:%0.3f Seconds]" % float(allEndTP - allStartTP))

