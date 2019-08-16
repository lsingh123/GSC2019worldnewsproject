#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 14:14:32 2019

@author: lavanyasingh
"""

import csv
import sys

def get_sources(infile="data/all_raw_cleaned.csv"):
    sources = []
    with open(infile, "r", errors = "ignore") as f:
        reader = csv.reader(f, delimiter = ",")
        for line in reader:
            sources.append(line[1])
        return sources

def read_urls(infile="data/urls.txt"):
    sources = get_sources()
    print(sources[0:10])
    not_found = []
    with open(infile, "r", errors = "ignore") as f:
        for line in f:
            line = line.replace("\n", "")
            if line not in sources:
                not_found.append(line)
    print(len(not_found))
    print(not_found)

def get_meta(infile="data/metadata.csv"):
    bad, html = [], []
    csv.field_size_limit(sys.maxsize)
    with open(infile, "r", errors = "ignore") as f:
        reader = csv.reader(f, delimiter = ",")
        for line in reader:
            total += 1
            if len(line) > 3:
                count += 1
            elif str(line[1]).find("upstream request timeout") != -1:
                bad.append(line)
            elif str(line[1]).find("HTTP Connection Pool") != -1:
                bad.append(line)
            elif str(line[1]).find("html") != -1:
                html.append(line)
    print(total, count)
    return bad, html

bad, html = get_meta()
        