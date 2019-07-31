#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 15:08:12 2019

@author: lavanyasingh
"""

import csv 

def clean_file(path):
    with open(path, mode = "r") as source:
        with open('ia_sources.csv', mode = "w") as output:
            r = csv.reader(source, delimiter = ',')
            (next(r))
            w = csv.writer(output, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
            w.writerow(['country', 'source url'])
            for line in r:
                w.writerow([line[7], line[2]])
                
clean_file(path)