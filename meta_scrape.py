#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 10:19:18 2019

@author: lavanyasingh
"""

from requests import Session
from lxml import etree
from urllib import parse
import concurrent.futures
import csv
import time
from bs4 import UnicodeDammit
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import argparse

# Scrape metadata from Kenji's service that returns rendered HTML


class MetadataParser():

    # optimal number of processes from `meta_test.py`
    def __init__(self, processes, retries=1, infile='data/all_raw_cleaned.csv', 
                 outfile='data/metadata.csv',):

        self.infile, self.outfile = infile, outfile
        self.processes, self.retries = processes, retries

        # create session and disable built in retries
        self.session = Session()
        retry = Retry(total=0)
        self.session.mount('http://', HTTPAdapter(max_retries=retry))

        # create HTML parser
        self.parser = etree.HTMLParser()

        # read in URLs
        self.urls = []
        self.read_in()

    # read in cleaned URLs from CSV
    def read_in(self):
        with open(self.infile, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            for line in reader:
                #for testing purposes
                if len(self.urls) > 50: break
                self.urls.append("http://" + "".join(line[1]))
        print("DONE READING")

    # load the HTML for a given URL
    def _load_url(self, url):
        url = parse.quote(url)
        try:
            r = self.session.get("http://crawl-services.us.archive.org:8200/web?url={url}&format=html".format(url=url),
                                 timeout=300)
        except TimeoutError as e:
            return str(e)
        html = r.text
        doc = UnicodeDammit(html, is_html=True)
        if not doc.unicode_markup:
            print("Failed to detect encoding for {url}".format(url=url))
        webfile = doc.unicode_markup.encode('utf-8')
        return webfile

    def load_url(self, url):
        webfile = self._load_url(url)
        for i in range(self.retries):
            if str(webfile).find("b'upstream request timeout'") != -1:
                print('retrying: {url}'.format(url=url))
                webfile = self._load_url(url)
            else:
                break
        return webfile

    # get open graph data for a given attribute (title, locale, description)
    def get_og(self, tree, attribute):
        try:
            query = "//meta[@property='og:{a}']/@content".format(a=attribute)
            return tree.xpath(query)[0]
        except IndexError:
            pass
        try:
            query = "//meta[@name='{a}']/@content".format(a=attribute)
            return tree.xpath(query)[0]
        except IndexError:
            pass
        try:
            query = "//meta[@name='twitter:{a}']/@value".format(a=attribute)
            return tree.xpath(query)[0]
        except IndexError:
            return None

    def get_title(self, tree):
        title = self.get_og(tree, 'title')
        if title is None:
            try:
                title = tree.xpath("//title")[0].text
            except IndexError:
                title = None
        return title

    def get_description(self, tree):
        desc = self.get_og(tree, 'decription')
        if desc is None:
            try:
                desc = tree.xpath("//meta[@name='description']/@content")[0]
            except IndexError:
                desc = None
        return desc

    # scrape and parse a given URL
    def _parse_url(self, url):
        html = self.load_url(url)
        tree = etree.fromstring(html, self.parser)
        title = self.get_title(tree)
        desc = self.get_description(tree)
        locale = self.get_og(tree, "locale")
        results = [url, title, desc, locale]
        if title is None and desc is None and locale is None:
            return [url, html]
        # replace none values with the empty string
        return ["" if res is None else res for res in results]

    def parse_url(self, url):
        return self._parse_url(url)

    def write_meta(self, results):
        with open(self.outfile, 'w') as outf:
            w = csv.writer(outf, delimiter=',', quotechar='"',
                           quoting=csv.QUOTE_MINIMAL)
            for url in results:
                w.writerow(url)
        print("WROTE ALL METADATA")

    def main(self):
        time1 = time.time()
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.processes) as executor:
            results = executor.map(self.parse_url, self.urls)
        time2 = time.time()
        self.write_meta(results)
        print(f"Took {time2-time1:.2f} seconds")
        self.session.close()
        return results


# create argument parser
def create_parser():
    argp = argparse.ArgumentParser(
            description='Scrape metadata from `all_raw_cleaned.csv')
    argp.add_argument('-p', '--processes', nargs='?', default=10, type=int,
                            help='number of workers to use. defaults to 15.')
    argp.add_argument('-inf', '--infile', nargs='?',
                      default='data/all_raw_cleaned.csv', type=str,
                      help='csv file to read URLs in from')
    argp.add_argument('-outf', '--outfile', nargs='?',
                      default='data/metadata.csv', type=str,
                      help='csv file to write metadata to')
    argp.add_argument('-r', '--retries', nargs='?',
                      default=1, type=int, help='number of retries')
    return argp


if __name__ == '__main__':
    argp = create_parser()
    args = argp.parse_args()
    parser = MetadataParser(infile=args.infile, outfile=args.outfile,
                            processes=args.processes, retries=args.retries)
    parser.main()
