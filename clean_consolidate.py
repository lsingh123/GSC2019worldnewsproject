#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 11:27:48 2019

@author: lavanyasingh
"""

import csv

# I used this script to consolidate the sources into one CSV file from all the 
# little ones I had. Those CSVs are no longer in this directory, as they have 
# already been consolidated. I'm leaving this script in for reference.

class consolidator():
    
    def __init__(self, outfile = 'data/all_raw.csv'):
        self.outfile = outfile
        
    # get metasource from path name
    def get_meta(self, path):
        return path.split('.')[0].replace('data/', '')
    
    # the US news data was structured differently from the rest of it 
    def us_news(self):
        with open('data/us_news.csv', 'r') as inf:
            reader = csv.reader(inf, delimiter=',')
            next(reader)
            with open(self.outfile, 'a+') as outf:
                w = csv.writer(outf, delimiter= ',', quotechar = '"', quoting = 
                               csv.QUOTE_MINIMAL)
                for line in reader:
                    w.writerow(['United States', line[2], line[1], 'English',
                                line[3], line[1], '', 'original', line[0], '', 
                                '', '', ''])
    
    # USNPL data was also structured differently
    def usnpl(self):
        with open('data/usnpl_wiki_list.csv', 'r') as inf:
            reader = csv.reader(inf, delimiter=',')
            next(reader)
            with open(self.outfile, 'a+') as outf:
                w = csv.writer(outf, delimiter= ',', quotechar = '"', quoting = 
                               csv.QUOTE_MINIMAL)
                for line in reader:
                    w.writerow(['United States', line[3], line[2], 'English', 
                                'Newspaper', line[2],'', 'usnpl', line[0], 
                                line[1], line[4], line[6], line[7]])

    # LION data was also structured differently
    def lion(self):
        with open('data/lion.csv', 'r') as inf:
            reader = csv.reader(inf, delimiter=',')
            next(reader)
            with open(self.outfile, 'a+') as outf:
                w = csv.writer(outf, delimiter= ',', quotechar = '"', quoting = 
                               csv.QUOTE_MINIMAL)
                for line in reader:
                    w.writerow(['United States', line[1], line[0], 'English', 
                                '', line[0], '', 'lion', line[5], line[4], '', 
                                '', ''])

    # reads in data that has been csv formatted (that I've cleaned before)
    def formatted(self, path):
        with open(path, 'r') as inf:
            reader = csv.reader(inf, delimiter=',')
            next(reader)
            with open(self.outfile, 'a+') as outf:
                w = csv.writer(outf, delimiter= ',', quotechar = '"', quoting = 
                               csv.QUOTE_MINIMAL)
                for line in reader:
                    row = line + ['' for n in range(9)]
                    row[7] = self.get_meta(path) 
                    w.writerow(row)
        print("DONE WITH ", path)

    # reads in data from a text file of URLS
    def txt(self, path):
        with open(path, 'r') as inf:
            with open(self.outfile, 'a+') as outf:
                w = csv.writer(outf, delimiter= ',', quotechar = '"', quoting = 
                               csv.QUOTE_MINIMAL)
                for line in inf:
                    row = [line if n == 1 else '' for n in range(12)]
                    row[7] = self.get_meta(path)
                    w.writerow(row)
        print ("DONE WITH ", path)
    
    def main(self):
        self.us_news()
        self.usnpl()
        self.lion()
        self.formatted('data/wikinews.csv')
        self.formatted('data/wikidata.csv')
        self.txt('data/topnews')
        self.formatted('data/newsgrabber.csv')
        self.txt('data/newscrawls')
        self.formatted('data/mediacloud.csv')
        self.formatted('data/inkdrop.csv')
        self.txt('data/gdelt')
        self.formatted('data/datastreamer.csv')
        
if __name__ == '__main__':
    consolidator = consolidator()
    consolidator.main()
    