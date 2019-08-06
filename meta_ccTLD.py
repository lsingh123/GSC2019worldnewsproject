#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 11:19:27 2019

@author: lavanyasingh
"""

import csv
from bs4 import BeautifulSoup
import requests
import helpers
import tldextract
import argparse


class countryGrabber():

    ENDPOINT = 'http://lavanya-dev.us.archive.org:3030/testwn/update'

    def __init__(self, inf, outf):
        self.countries = self.get_cc()
        self.country_ids = helpers.get_countries()

    # scrape CCTLDs from the ICANN Wiki
    # returns a dict in {code:country name} format
    def get_cc(self):
        page = 'https://icannwiki.org/Country_code_top-level_domain'
        countries = {}
        response = requests.get(page)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.find('table').find_all('tr')[1:]
        for row in data:
            code = row.find_all('td')[0].find('a')['title'][1:]
            country = row.find_all('td')[1].contents[0]
            countries[code] = country
        return countries

    # extract CCTLD from url
    def find_cc(self, url):
        tld = tldextract.extract(url)[2]
        if tld.find('.') != -1:
            tld = tld[tld.find('.')+1:]
        if tld in self.countries:
            return self.countries[tld]
        return None

    # assign each source a country based on CCTLD
    def assign_cc(self):
        sources = helpers.read_in(self.infile)
        for source in sources:
            country = self.find_cc(source[1])
            if country is not None:
                source[0] = country
        return sources

    def write_cc(self):
        sources = self.assign_cc()
        with open(self.outfile, "w", errors="ignore") as f:
            w = csv.writer(f, delimiter=',', quotechar='"',
                           quoting=csv.QUOTE_MINIMAL)
            w.writerow(['country', 'source url', 'title', 'language', 'type',
                        'title native language', 'paywall', 'metasource',
                        'state', 'town', 'wikipedia name', 'redirects?',
                        'wikipedia link'])
            for item in sources:
                w.writerow(item)


# create argument parser
def create_parser():
    argp = argparse.ArgumentParser(
            description='Determine country of URL from CCTLD')
    argp.add_argument('-inf', '--infile', nargs='?',
                      default='data/all_raw_cleaned.csv', type=str,
                      help='csv file to read URLs in from')
    argp.add_argument('-outf', '--outfile', nargs='?',
                      default='data/all_raw_cleaned.csv', type=str,
                      help='csv file to write metadata to')
    return argp


if __name__ == '__main__':
    argp = create_parser()
    args = argp.parse_args()
    grabber = countryGrabber(inf=args.infile, outf=args.outfile)
    grabber.write_cc()
