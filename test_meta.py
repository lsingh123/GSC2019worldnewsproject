#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 15:49:40 2019

@author: lavanyasingh
"""

from requests_html import HTMLSession
from lxml import etree
from io import StringIO
from urllib import parse
import concurrent.futures
import csv
import time
from bs4 import UnicodeDammit

url = "http://nytimes.com"
session = HTMLSession()
r = session.get("http://crawl-services.us.archive.org:8200/web?url={url}&format=html".format(url=url))
html = r.html.html
doc = UnicodeDammit(html, is_html=True)
if not doc.unicode_markup:
    print ("ERR. UnicodeDammit failed to detect encoding, tried [%s]", \
                ', '.join(doc.triedEncodings))
webfile = doc.unicode_markup.encode('utf-8')
parser = etree.HTMLParser()
root = etree.fromstring(webfile, parser=parser)
query = "//meta[@property='og:title']/@content"
print(root.xpath(query)[0])