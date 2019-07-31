#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 13:10:42 2019

@author: lavanyasingh
"""

from bs4 import BeautifulSoup
import csv
import time
import os
os.chdir(os.path.dirname(os.getcwd()))
from pyppeteer import launch
import asyncio
import logging
import sys
import traceback
import tracemalloc

tracemalloc.start()

logger = logging.getLogger('__worldnews__')
logging.basicConfig(filename='logfle.log',filemode = 'w')

def my_handler(type, value, tb):
    logger.exception("Uncaught exception: {0}".format(str(value)))

# Install exception handler
sys.excepthook = my_handler

class FBOGCrawler():

    PATH = os.getcwd() + "/data/raw"

    def __init__(self):
        self.res, self.urls = [], []
        self.read_in()
        self.count = 0

    def read_in(self):
        with open(self.PATH + "/all_raw_cleaned.csv", 'r') as f:
            reader = csv.reader(f, delimiter=',')
            for line in reader:
                if len(self.urls) > 10: break
                self.urls.append("http://" + "".join(line[1]))
        print("DONE READING")
    
    # finds FBOG or Twitter Card metadata for a given attribute
    def get_attr(self, head, attr):
        try:
            return head.find(attrs={"property": "og:" + attr})['content']
        except TypeError:
            pass
        try:
            return head.find(attrs={"property": "twitter:" + attr})['content']
        except TypeError:
            pass
        try:
            return head.find("title").text
        except AttributeError:
            return ""

    # finds FBOG locale metadata
    def get_locale(self, head):
        try:
            return head.find(attrs={"property": "og:locale"})['content']
        except TypeError:
            return ""
        
    async def get_browser(self):
        return await launch({"headless": False, "args": ['--nosandbox']})
    
    # returns page html
    async def get_page(self, browser, url):
        print(self.count)
        page = await browser.newPage()
        await page.goto(url, timeout = 100000)
        await page.waitFor("head")
        c = await page.content()
        await page.close()
        return c
    
    # returns url, page title, page description, page locale 
    async def parse_html(self, url):
        try:
            html = await self.get_page(url)
            if html == "": return [url, "TIMEOUTERROR"]
            soup = BeautifulSoup(html, features="html.parser")
            head = soup.head
            title = self.get_attr(head, "title")
            desc = self.get_attr(head, "description")
            locale = self.get_locale(head)
            return [url, title, desc, locale]
        except Exception as e:
            logger.exception(traceback.format_exc())
            return [url, str(e)]
        
    # scrapes all pages
    async def parse_all(self):
        self.browser = await self.get_browser()
        res = await asyncio.gather(*(self.parse_html(url) for url in self.urls), 
                                   return_exceptions = True)
        await self.browser.close()
        return res
        
    def write_meta(self):
        with open(self.PATH + "/meta_good3.csv", 'w') as outf:
            w = csv.writer(outf, delimiter=',', quotechar='"',
                           quoting=csv.QUOTE_MINIMAL)
            for url in self.res:
                w.writerow(url)
        print("WROTE ALL METADATA")

    def main(self):
        time1 = time.time()
        self.res = asyncio.run(self.parse_all())
        print(self.res)
        time2 = time.time()
        print(f"Took {time2-time1:.2f} s")
        self.write_meta()

if __name__ == "__main__":
    crawler = FBOGCrawler()
    crawler.main()
    print("FINISHED RUNNING")
