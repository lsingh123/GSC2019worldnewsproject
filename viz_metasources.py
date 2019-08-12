#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 16:57:46 2019

@author: lavanyasingh
"""

import csv
from matplotlib import pyplot as plt

infile = "data/all_raw_cleaned.csv"

def read_in():
    sources = []
    with open(infile, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            for line in reader:
                sources.append([line[1], line[7].split(" ")])
    print("DONE READING")  
    return sources

def make_data():
    sources = read_in()
    data = {}
    for source in sources:
        metasources = source[1]
        for ms in metasources:
            ms.replace("kk", "k").replace(".com", "")
            if ms != "": 
                try:
                    data[ms] += 1
                except KeyError:
                    data.update({ms:1})
    datalist = [(val, key) for key, val in data.items()]

    top = sorted(datalist, reverse=True)
    print(top)
    
    y = [element[1] for element in top]
    x = [element[0] for element in top]
    
    plt.bar(y, x, align='center', alpha=0.5)
    plt.ylabel('Metasource')
    plt.xticks(y, y, rotation='vertical')
    plt.show()
    
if __name__ == '__main__':
    make_data()