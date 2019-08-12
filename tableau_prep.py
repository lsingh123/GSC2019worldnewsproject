#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 09:56:27 2019

@author: lavanyasingh
"""

import csv
from fuzzywuzzy import process
import helpers
import argparse
import random

class mapDataMaker():
    
    def __init__(self, countryfile = "data/countries.csv", 
                 infile = "data/all_raw_cleaned1.csv",
                 outfile = "data/geodata.csv"):
        self.countryfile = countryfile
        self.infile, self.outfile = infile, outfile
    
    # returns a dictionary {country name: [iso, latitude, longitude, name]}
    def read_countries(self):
        countries = {}
        with open(self.countryfile, 'r') as inf:
            reader = csv.reader(inf, delimiter=',')
            next(reader)
            for line in reader:
                countries.update({line[3]: line})
        return countries
    
    def process_geo(self):
        countries = self.read_countries()
        total = 0
        with open(self.infile, 'r') as inf, open(self.outfile, 'w') as outf:
            reader = csv.reader(inf, delimiter=',')
            w = csv.writer(outf, delimiter= ',', quotechar = '"', 
                               quoting = csv.QUOTE_MINIMAL)
            w.writerow(["ISO Code", "Latitude", "Longitude", "Country", 
                        "URL", "Title"])

            for line in reader:
                total += 1
                # skip entries with broken country values
                if helpers.is_bad(line[0]): continue

                country = process.extract(line[0], list(countries.keys()), 
                                          limit = 1)[0][0]
                print(str(total),end="\r")
                row = countries[country] + [line[1]]
                w.writerow(row)
    
    def process(self):
        total = 0
        size = 1000000
        random.seed()
        countries = []
        with open(self.infile, 'r') as inf, open(self.outfile, 'w') as outf:
            reader = csv.reader(inf, delimiter=',')
            w = csv.writer(outf, delimiter= ',', quotechar = '"', 
                               quoting = csv.QUOTE_MINIMAL)
            w.writerow(["Country", "URL", "Title", "Size"])

            for line in reader:
                total += 1
                print(str(total),end="\r")
                
                # skip entries with broken titles
                if helpers.is_bad(line[2]): continue
            
                # skip countries we've already seen and bad countries
                if line[0] in countries or helpers.is_bad(line[0]): continue
            
                size = size / 1.05
                
                if total < 5:
                    size = size * 5

                try:
                    int(line[2].replace("Q", "")[0:3])
                    continue
                except:
                    countries.append(line[0])
    
                    row = [line[0], line[1], line[2], size]
                    w.writerow(row)
    
    def main(self, process):
        if process == "process":
            self.process()
        elif process == "geo":
            self.process_geo()

# create argument parser
def create_parser():
    argp = argparse.ArgumentParser(
            description='Prep country data for Tableau')
    argp.add_argument('-inf', '--infile', nargs='?',
                      default='data/all_working.csv', type=str,
                      help='csv file to read URLs in from')
    argp.add_argument('-outf', '--outfile', nargs='?',
                      default='data/geodata2.csv', type=str,
                      help='csv file to write metadata to')
    argp.add_argument('-p', '--process', nargs='?', choices = ['geo', 'process'],
                      default='process', type=str,
                      help='geo for geoprocessing and process for text processing')
    return argp

if __name__ == '__main__':
    argp = create_parser()
    args = argp.parse_args()
    mapMaker = mapDataMaker(infile=args.infile, outfile=args.outfile)
    mapMaker.main(args.process)        
        
    
    
    
    