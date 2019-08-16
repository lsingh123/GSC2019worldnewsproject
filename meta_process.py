#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 10:01:49 2019

@author: lavanyasingh
"""

# a script to clean the results of meta_scrape.py and retry failed links

import csv
from meta_scrape import MetadataParser
import sys

def get_meta(infile='data/metadata.csv', outfile='data/metadata_cleaned.csv'):
    bad = []
    total = 0
    csv.field_size_limit(sys.maxsize)
    parser = MetadataParser(in_urls=[])
    with open(infile, "r", errors = "ignore") as inf, open(outfile, 'w') as outf:
        reader = csv.reader(inf, delimiter = ",")
        w = csv.writer(outf, delimiter= ',', quotechar = '"', 
                           quoting = csv.QUOTE_MINIMAL)
        for line in reader:
            total += 1
            if len(line) > 3:
                w.writerow(line)
            elif (str(line[1]).find("upstream request timeout") != -1 or 
                  str(line[1]).find("HTTP Connection Pool") != -1):
                bad.append(line[0])
            elif str(line[1]).find("html") != -1:
                line = parser.parse_url(line[0], html=str(line[1]))
                w.writerow(line)
            print(str(total), end = "\r")
    print("DONE PARSING {total} URLs".format(total=total))
    return bad

def fix_bad():
    bad = get_meta()
    parser = MetadataParser(in_urls=bad, outfile="data/metadata_cleaned.csv",
                            retries=3)
    parser.main()
    
if __name__ == '__main__':
    fix_bad()