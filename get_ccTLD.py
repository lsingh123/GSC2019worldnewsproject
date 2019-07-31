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
import os
os.chdir(os.path.dirname(os.getcwd()))

path = 'data/raw/all_raw_cleaned.csv'

class countryGrabber():
    
    q_endpoint = 'http://lavanya-dev.us.archive.org:3030/testwn/query'
    u_endpoint = 'http://lavanya-dev.us.archive.org:3030/testwn/update'
        
    endpoint_url = u_endpoint

    def __init__(self, path):
        self.countries = self.get_cc()
        self.path = os.getcwd() + path
        self.country_ids = helpers.get_countries()
        
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
        
    def find_cc(self, url):
        tld = tldextract.extract(url)[2]
        if tld.find('.') != -1:
            tld = tld[tld.find('.')+1:]
        if tld in self.countries:
            return self.countries[tld]
        return None
    
    def assign_cc(self):
        sources = helpers.read_in(self.path)
        for source in sources:
            country = self.find_cc(source[1])
            if country != None: 
                source[0] = country
        return sources
    
    def write_cc(self):
        sources = self.assign_cc()
        with open(path, "w", errors = "ignore") as f:
            w = csv.writer(f, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
            w.writerow(['country', 'source url', 'title', 'language', 'type', 'title native language',
                        'paywall', 'metasource', 'state', 'town', 'wikipedia name', 'redirects?',
                        'wikipedia link'])
            for item in sources:
                w.writerow(item)        


