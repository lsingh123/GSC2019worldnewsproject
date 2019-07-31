#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 09:56:27 2019

@author: lavanyasingh
"""

import csv
import os
from fuzzywuzzy import process
import helpers

class mapDataMaker():
    
    def __init__(self, path = os.path.dirname(os.getcwd()), 
                 countryfile = "/data/countries.csv", 
                 infile = "/data/all_raw_cleaned1.csv",
                 outfile = "/data/geodata.csv"):
        self.countryfile, self.path = countryfile, path
        self.infile, self.outfile = self.path + infile, self.path + outfile
        self.countries = self.read_countries()
    
    # returns a dictionary {country name: [iso, latitude, longitude, name]}
    def read_countries(self):
        countries = {}
        with open(self.path + self.countryfile, 'r') as inf:
            reader = csv.reader(inf, delimiter=',')
            next(reader)

            for line in reader:
                countries.update({line[3]: line})
        return countries
    
    def process(self):
        total = 0

        with open(self.infile, 'r') as inf, open(self.outfile, 'w') as outf:

            reader = csv.reader(inf, delimiter=',')
            w = csv.writer(outf, delimiter= ',', quotechar = '"', 
                               quoting = csv.QUOTE_MINIMAL)
            w.writerow(["ISO Code", "Latitude", "Longitude", "Country", "URL"])

            for line in reader:
                total += 1
                # skip entries with broken country values
                if helpers.is_bad(line[0]): continue

                country = process.extract(line[0], list(self.countries.keys()), 
                                          limit = 1)[0][0]
                print(str(total),end="\r")
                row = self.countries[country] + [line[1]]
                w.writerow(row)
                    

if __name__ == '__main__':
    mapMaker = mapDataMaker()
    mapMaker.process()        
        
    
    
    
    