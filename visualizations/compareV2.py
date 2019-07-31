#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 15:20:50 2019

@author: lavanyasingh
"""

import csv
from matplotlib import pyplot as plt
from matplotlib_venn import venn2, venn2_circles, venn3, venn3_circles
import os 

os.getcwd()
os.chdir('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/')


#count number of entries per country 
def count_sources_old(path):
    total = {}
    with open(path, 'r', errors = 'ignore') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        first = next(reader)
        country = first[0]
        count = 1
        for line in reader:
            line_c = line[0]
            if country != line_c: 
                total[country] = count
                count = 0
                country = line_c
            count += 1
        total[country] = count
    return total

#count number of entries per country 
def count_sources(path):
    total = {}
    with open(path, 'r', errors = 'ignore') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        count = 1
        for line in reader:
            if line[0] in total:
                total[line[0]] += 1
            else:
                total[line[0]] = 1
            count += 1
    return total

#graph counts per metasource
def compare_counts():
    mc = count_sources("data/mc_sources.csv")
    ia = count_sources("data/ia_sources.csv")
    wd = count_sources("data/wd_sources.csv")
    mc_count = []
    ia_count = []
    wd_count = []
    countries = []
    for country in ia:
        if country in wd and country in mc:
            ia_count.append(ia[country])
            mc_count.append(mc[country])
            wd_count.append(wd[country])
            countries.append(country)
    fig, ax = plt.subplots(3, sharex = "col", sharey = "col")
    ax[0].set_title("No. of Sources by Country")
    ax[0].set_ylabel("media cloud")
    ax[1].set_ylabel("internet archive")
    ax[2].set_ylabel("wikidata")
    ax[2].set_xlabel("country")
    ax[0].bar(countries, mc_count)
    ax[1].bar(countries, ia_count)
    ax[2].bar(countries, wd_count)
    ax[2].set_xticks([])

#read all sources in from a CSV in country: [source list] format
def get_sources(path):
    with open(path, "r", errors = "ignore") as f:
        reader = csv.reader(f, delimiter = ",")
        next(reader)
        sources = {}
        for line in reader:
            if line[0] in sources:
                sources[line[0]].append(line[1])
            else:
                sources[line[0]] = [line[1]]
    return sources
    
# returns a dict in country: [source list] format of overlapping URLs
def find_overlap(s1, s2):
    overlap = {}
    for country in s1:
        if country in s2:
            overlap[country] = []
            for url in s1[country]:
                if url in s2[country]: overlap[country].append(url)
    return overlap

# returns a list of overlapping URLs given two dictionaries in country: [source list] format
def find_total_overlap(d1, d2):
    odict = find_overlap(d1, d2)
    overlap = []
    for country in odict:
        for url in odict[country]:
            overlap.append(url)
    return overlap

    

#counts number of lines in a csv (excluding header)
def get_count(path):
    with open(path, "r") as f:
        reader = csv.reader(f, delimiter = ",")
        next(reader)
        count = 0
        for line in reader:
            count +=1
    return count

#turns a dict of lists to one giant list 
def dict_to_list(dict):
    l = []
    for item in dict.values():
        l.extend(item)
    return l

#make a venn diagram documenting the overlap in URLs for each metasource
def compare_overlap():
    ia_path = "data/ia_sources.csv"
    mc_path = "data/mc_sources.csv"
    wd_path = "data/wd_sources.csv"
    ia_list = set(dict_to_list(get_sources(ia_path)))
    mc_list = set(dict_to_list(get_sources(mc_path)))
    wd_list = set(dict_to_list(get_sources(wd_path)))
    venn3([ia_list, mc_list, wd_list], ('Internet Archive', 'Media Cloud', 'Wikidata'))
    plt.savefig("IA v MC v WD.png")

def compare_2():
    mc_path = "data/mc_sources_meta.csv"
    ds_path = "data/ds_sources_truncated.csv"
    mc_list = set((get_sources(mc_path)))
    ds_list = set((get_sources(ds_path)))
    venn2([mc_list, ds_list], ('Media Cloud', 'DataStreamer'))
    plt.savefig('mc vs ds.png')
    
compare_2()

            
            