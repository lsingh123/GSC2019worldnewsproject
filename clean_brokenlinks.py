#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 12:45:23 2019

@author: lavanyasingh
"""
# script to filter out broken links

import csv

def get_codes():
    codes = {}
    with open("data/codes2.csv", 'r') as inf:
        reader = csv.reader(inf, delimiter=',')
        for line in reader:
            if line[1] != "ERROR":
                code = int(line[1])
            try:
                redirect = line[2]
            except IndexError:
                redirect = None
            codes.update({line[0]:[code, redirect]})
    return codes

def write_codes():
    codes = get_codes()
    count = 0
    with open("data/all_raw_cleaned.csv", 'r') as inf, \
        open("data/all_working.csv", 'w') as outf:
        reader = csv.reader(inf, delimiter=',')
        w = csv.writer(outf, delimiter= ',', quotechar = '"', 
                           quoting = csv.QUOTE_MINIMAL)
        for line in reader:
            code = codes['http://' + line[1]]
            if int(code[0]) < 400:
                count += 1
                line[11] = code[1]
                w.writerow(line)
    print(count)
                
write_codes()