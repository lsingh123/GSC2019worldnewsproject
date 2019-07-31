#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 10:26:48 2019

@author: lavanyasingh
"""

from requests_html import HTMLSession
import csv
import os

class countryScraper():
    
    def __init__(self, outfile = os.path.dirname(os.getcwd()) + "/data/countries.csv"):
        self.outfile = outfile
        self.url = 'https://developers.google.com/public-data/docs/canonical/countries_csv'
    
    def scrape(self):
        session = HTMLSession()
        response = session.get(self.url)
        response.html.render()
        table = response.html.find('table')[0]
        countries = []
        for row in table.find('tr')[1:]:
            countries.append([element.text for element in row.find('td')])
        return countries
    
    def write(self, countries):
        with open(self.outfile, 'w') as outf:
            w = csv.writer(outf, delimiter= ',', quotechar = '"', 
                               quoting = csv.QUOTE_MINIMAL)
            w.writerow(["Code", "Latitude", "Longitude", "Name"])
            for row in countries:
                w.writerow(row)

if __name__ == "__main__":
    scraper = countryScraper()
    countries = scraper.scrape()
    scraper.write(countries)

