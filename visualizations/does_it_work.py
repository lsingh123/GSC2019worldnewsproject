#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 15:29:34 2019

@author: lavanyasingh
"""

import os
import requests
import csv

#read all sources in from a CSV in [source list] format
def get_sources(path):
    with open(path, "r", errors = "ignore") as f:
        reader = csv.reader(f, delimiter = ",")
        next(reader)
        sources = []
        for line in reader:
            sources.append(line[1])
    return sources

def does_it_work(path):
    sources = get_sources(path)
    total,count = 0, 0
    for url in sources:
        total +=1
        try: 
            requests.get(url, stream = True)
        except Exception as e:
            count +=1
            print(e)
    print('total', total)
    print('count', count)
    
does_it_work('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/data/ds_sources_truncated.csv')