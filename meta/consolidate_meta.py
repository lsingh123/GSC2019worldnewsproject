#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 09:44:44 2019

@author: lavanyasingh
"""

import csv
import os
os.chdir(os.path.dirname(os.getcwd()))
import helpers

#returns a dict in url: [title, description, locale] format
def read_meta():
    sources = {}
    total, good = 0, 0
    with open("data/raw/meta_good.csv", 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            total += 1
            try:
                sources.update({line[0]: [line[1], line[2], line[3]]})
                good += 1
            except KeyError:
                None
    print("DONE READING", total, good)
    return sources

#returns a dict in url: [code, *redirect] format
def read_codes():
    sources = {}
    total, good = 0, 0
    with open("data/raw/codes9.csv", 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            total += 1
            sources.update({line[0]: [line[1], line[2]]})
            if line[1] != "ERROR": good +=1 
    print("DONE READING", total, good)
    return sources

def read_in():
    sources = {}
    total = 0
    with open("data/raw/all_raw_cleaned3.csv", 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            total += 1
            sources.update({"http://" + "".join(line[1]):line})
    print("DONE READING")
    return sources 
   
codes = read_codes()
meta = read_meta()
sources = read_in()

# return a dict in url:redirect format
def get_good():
    good = {}
    for url in sources:
        if url in codes or url in meta: 
            good.update({url:codes[url][1]})
    return good

good = get_good()

def make_cleaned():
    cleaned = []
    for url in sources:
        line = sources[url]
        if url in good:
            line.append(codes[url][1])
            line.append(meta[url][1])
            if helpers.is_bad(line[2]) or line[7].find("original") == -1:
                line[2] = meta[url][0]
            cleaned.append(line)
    return cleaned

cleaned = make_cleaned()

def write_cleaned():
    with open('data/raw/all_cleaned4.csv', 'w') as outf:
        w = csv.writer(outf, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        for line in cleaned:
            w.writerow(line)
    print("WROTE ALL SOURCES")   
            
write_cleaned()


    