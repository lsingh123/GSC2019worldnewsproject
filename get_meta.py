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

    def read_in(self):
        with open(self.PATH + "/all_raw_cleaned.csv", 'r') as f:
            reader = csv.reader(f, delimiter=',')
            for line in reader:
                if len(self.urls) > 50: break
                self.urls.append("http://" + "".join(line[1]))
        print("DONE READING")
    
    async def get_browser(self):
        return await launch({"headless": True, "args": ['--nosandbox']})
    
    async def get_page(self, browser, url):
        try:
            page = await browser.newPage()
            await page.goto(url, timeout = 100000)
            await page.waitFor("head")
            c = await page.content()
            await page.close()
            return c
        except Exception: 
            raise
    
    async def parse_html(self, browser, url):
        try:
            html = await self.get_page(browser, url)
            soup = BeautifulSoup(html, features="html.parser")
            head = soup.head
            title = self.get_attr(head, "title")
            desc = self.get_attr(head, "description")
            locale = self.get_locale(head)
            return [url, title, desc, locale]
        except TimeoutError:
            raise
        except Exception as e:
            raise
            #logger.exception(traceback.format_exc())
            return [url, str(e)]

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

    def get_locale(self, head):
        try:
            return head.find(attrs={"property": "og:locale"})['content']
        except TypeError:
            return ""
        
    async def parse_all(self):
        browser = await self.get_browser()
        for url in self.urls:
            try:
                self.res.append(await self.parse_html(browser, url))
                print(str(len(self.res)),end="\r")
            except Exception as e:
                print(url, e)
                browser = await self.get_browser()
        await browser.close()
    
    def callback(self, fut):
        try:
            fut.result()
        except Exception as e:
            print(e)
            raise
        
    def write_meta(self):
        with open(self.PATH + "/meta_good2.csv", 'w') as outf:
            w = csv.writer(outf, delimiter=',', quotechar='"',
                           quoting=csv.QUOTE_MINIMAL)
            for url in self.res:
                w.writerow(url)
        print("WROTE ALL METADATA")

    def main(self):
        loop = asyncio.get_event_loop()
        time1 = time.time()
        loop.run_until_complete(self.parse_all())
        time2 = time.time()
        print(f"Took {time2-time1:.2f} s")
        self.write_meta()

if __name__ == "__main__":
    crawler = FBOGCrawler()
    crawler.main()
    print("FINISHED RUNNING")
