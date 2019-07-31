#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 11:53:52 2019

@author: lavanyasingh
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 15:20:50 2019

@author: lavanyasingh
"""

import csv
from matplotlib import pyplot as plt
from matplotlib_venn import venn2, venn2_circles, venn3, venn3_circles
from simple_venn import venn4
import os

os.getcwd()
os.chdir('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/')

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

#read all sources in from a CSV in [source list] format
def get_sources(path):
    count = 0 
    with open(path, "r", errors = "ignore") as f:
        reader = csv.reader(f, delimiter = ",")
        next(reader)
        sources = []
        for line in reader:
            count +=1
            sources.append(line[1])
    print(count, path)
    return sources

    
#counts number of lines in a csv (excluding header)
def get_count(path):
    with open(path, "r") as f:
        reader = csv.reader(f, delimiter = ",")
        next(reader)
        count = 0
        for line in reader:
            count +=1
    return count

#make a venn diagram documenting the overlap in URLs for each metasource
def compare_overlap(path_list, label_list, title):
    source_list = [set(get_sources(x)) for x in path_list]
    venn3(source_list, label_list)
    plt.savefig(title)
    
ia_path = "ia_sources.csv"
mc_path = "mc_sources_meta.csv"
wd_path = "wd_sources.csv"
ink_path = "inkdrop_sources.csv"
ds_path = "data/ds_sources_truncated.csv"
ia = "Internet Archive"
mc = "Media Cloud"
wd = "Wikidata"
ink = "Inkdrop"

def test(path_list, label_list):
    source_list = [set(get_sources(x)) for x in path_list]
    venn2(source_list, label_list)

def compare_2():
    mc_path = "data/mc_sources_meta.csv"
    ds_path = "data/ds_sources_truncated.csv"
    mc_list = set((get_sources(mc_path)))
    ds_list = set((get_sources(ds_path)))
    venn2([mc_list, ds_list], ('Media Cloud', 'DataStreamer'))
    plt.savefig('mc vs ds.png')

compare_2()
            