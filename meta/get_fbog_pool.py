#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 12:58:07 2019

@author: lavanyasingh
"""

from multiprocessing import Pool
from bs4 import BeautifulSoup
import csv
from requests_html import HTMLSession
import time
import os
os.chdir(os.path.dirname(os.getcwd()))

class FBOGCrawler():

    PATH = os.getcwd() + "/data/raw"

    def __init__(self, processes):
        self.res, self.urls = [], []
        self.session = HTMLSession()
        self.read_in()
        self.processes = processes
        self.count = 0

    def read_in(self):
        with open(self.PATH + "/all_raw_cleaned.csv", 'r') as f:
            reader = csv.reader(f, delimiter=',')
            for line in reader:
                # for testing purposes
                #if len(self.urls) > 100: break
                self.urls.append("http://" + "".join(line[1]))
        print("DONE READING")

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

    def get_meta(self, url):
        self.count += 1
        try:
            response = self.session.get(url, timeout=30)
            soup = BeautifulSoup(response.html.html, features="html.parser")
            head = soup.head
            title = self.get_attr(head, "title")
            desc = self.get_attr(head, "description")
            locale = self.get_locale(head)
            self.res.append([url, title, desc, locale])
        except Exception as e:
            self.res.append([url, str(e)])
        if self.count % 1000 == 0: print(self.count)

    def write_meta(self):
        with open(self.PATH + "/meta_good.csv", 'w') as outf:
            w = csv.writer(outf, delimiter=',', quotechar='"',
                           quoting=csv.QUOTE_MINIMAL)
            for url in self.res:
                w.writerow(url)
        print("WROTE ALL META")

    def main(self):
        p = Pool(processes=self.processes)
        time1 = time.time()
        p.map(self.get_meta, self.urls)
        p.close()
        p.join()
        time2 = time.time()
        print(f"Took {time2-time1:.2f} s")
        self.write_meta()
        self.session.close()

if __name__ == "__main__":
    #after testing, 9 is the optimal number of processes on lavanya-dev VM
    crawler = FBOGCrawler(processes=8)
    crawler.main()
    print("FINISHED RUNNING")
