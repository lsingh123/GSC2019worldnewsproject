#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 10:02:55 2019

@author: lavanyasingh
"""

# script to prepare data for the cohort of Berkeley interns 

import csv
from fuzzywuzzy import fuzz
import helpers

INFILE = 'data/all_raw_cleaned.csv'
OUTFILE = 'data/bolivia sources.csv'

def write_filtered(filter_fun, index):
    '''
    reads rows in from INFILE
    takes a filter function as first argument, of type string->bool
    takes index to filter on as second argument, of type int
    writes filtered records to OUTFILE
    '''
    total = 0
    with open(INFILE, 'r') as inf, open(OUTFILE, 'w') as outf:
        reader = csv.reader(inf, delimiter=',')
        w = csv.writer(outf, delimiter=',', quotechar='"', 
                       quoting=csv.QUOTE_MINIMAL)
        for line in reader:
            if filter_fun(line[index]):
                total += 1
                w.writerow(line)
        print(f"WROTE {total} LINES")

def bolivia_filter(country):
    r = fuzz.ratio(country, "Bolivia")
    return r > 75

if __name__ == '__main__':
    write_filtered(bolivia_filter, 0)