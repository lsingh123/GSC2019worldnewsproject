#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 15:09:18 2019

@author: lavanyasingh
"""

#investigating why there's such little overlap between datastreamer and media cloud's sources

import os
import csv
from matplotlib_venn import venn2, venn2_circles, venn3, venn3_circles
from truncate import truncate


os.getcwd()
os.chdir('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/')

mc_path = "data/mc_sources_meta.csv"
ds_path = "data/ds_sources_truncated.csv"
ink_path = 'data/inkdrop_sources.csv'
ia_path = 'data/ia_sources.csv'

#read all sources in from a CSV in [source list] format
def get_sources(path):
    with open(path, "r", errors = "ignore") as f:
        reader = csv.reader(f, delimiter = ",")
        next(reader)
        sources = []
        for line in reader:
            url = truncate(line[1])
            if url not in sources:
                sources.append(url)
    return sources

def compare_2():
    mc_list = set((get_sources(ia_path)))
    ds_list = set((get_sources(ds_path)))
    venn2([mc_list, ds_list], ('Ink', 'DataStreamer'))
    plt.savefig('mc vs ds.png')
    

def manual_overlap():
    overlap = 0
    mc_list = get_sources(mc_path)
    ds_list = get_sources(ds_path)
    for source in mc_list:
        if source in ds_list:
            overlap += 1
    print(overlap)

compare_2()
