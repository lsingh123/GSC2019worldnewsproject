#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 15:10:29 2019

@author: lavanyasingh
"""

import csv
import pycountry
import numpy
from matplotlib import pyplot as plt


#compare our sources to mc's sources
#TODO: BROKEN
def compare_sources():
    overlap = {}
    with open('data/World News Sources - World News Sources.csv', 'r', errors = 'ignore') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        first = next(reader)
        country = pycountry.countries.get(name = first[7]).alpha_2
        count = 0
        if first[2] in media[country]: count += 1
        for line in reader:
            line_c = pycountry.countries.get(name = (line[7]).strip()).alpha_2
            if country == line_c: 
                overlap[country] = count
                count = 0
                country = line_c
            if line[2] in media[country]: count += 1
        overlap[country] = count
    return overlap

#count number of entries per country from our spreadsheet
def count_sources():
    total = {}
    with open('World News Sources - World News Sources.csv', 'r', errors = 'ignore') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        first = next(reader)
        country = first[7]
        count = 1
        for line in reader:
            line_c = line[7].strip()
            if country != line_c: 
                total[country] = count
                count = 0
                country = line_c
            count += 1
        total[country] = count
    return total

#count number of entries per country for mc 
def count_sources_mc():
    total = {}
    with open('mc_sources.csv', 'r', errors = 'ignore') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        first = next(reader)
        country = first[0]
        count = 1
        for line in reader:
            line_c = line[0].strip()
            if country != line_c: 
                total[country] = count
                count = 0
                country = line_c
            count += 1
        total[country] = count
    return total

#compare our counts to their counts
def compare_counts():
    count_mc = count_sources_mc()
    count_ia = count_sources()
    diffs = {}
    for item in count_ia:
        if item in count_mc: diffs[item] = count_mc[item] - count_ia[item]
    return diffs

#analyze differences between our counts and media cloud's
def analyze_diffs():
    count_mc = count_sources_mc()
    count_ia = count_sources()
    mc = []
    ia = []
    diff = []
    c = []
    diffs = compare_counts()
    for key in diffs:
        mc.append(count_mc[key])
        ia.append(count_ia[key])
        diff.append(diffs[key])
        c.append(key)
    fig,ax = plt.subplots(1)
    ax.bar(c, mc, color = 'b')
    ax.bar(c, ia, color = 'k')
    ax.bar(c, diff, color = 'r')
    ax.set_xticks([])
    plt.title("IA's News Sources vs. Media Cloud's News Sources")
    plt.legend()
    plt.savefig("diffs.png")
    print(numpy.corrcoef(diff, mc))
    print(numpy.corrcoef(diff, ia))

analyze_diffs()