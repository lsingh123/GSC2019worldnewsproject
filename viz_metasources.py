#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 16:57:46 2019

@author: lavanyasingh
"""

import csv
from matplotlib import pyplot as plt

class Viz_Maker:

    def __init__(self, infile="data/all_raw_cleaned.csv"):
        self.infile=infile
    
    def read_in(self):
        sources = []
        with open(self.infile, 'r') as f:
                reader = csv.reader(f, delimiter=',')
                for line in reader:                    
                    sources.append([line[1], line[7].split(" ")])
        print("DONE READING")  
        return sources
    
    def ms_bar_chart(self):
        sources = self.read_in()
        data = {}
        for source in sources:
            metasources = source[1]
            for ms in metasources:
                if ms != "": 
                    try:
                        data[ms] += 1
                    except KeyError:
                        data.update({ms:1})
        datalist = [(val, key) for key, val in data.items()]
    
        top = sorted(datalist, reverse=True)
        
        y = [element[1] for element in top]
        x = [element[0] for element in top]
        
        plt.bar(y, x, align='center', alpha=1, color="#141d99")
        plt.xlabel('Metasources', fontsize=15)
        plt.ylabel('Number of Sources', fontsize = 15)
        plt.xticks(y, y, rotation='vertical')
        plt.box(False)
        plt.tick_params(axis='both', length = 0)
        plt.locator_params(axis='y', nbins=4)
        plt.title("World News Project Metasources", fontsize=18)
        plt.tight_layout()
        plt.show()
    
if __name__ == '__main__':
    viz_maker = Viz_Maker()
    viz_maker.ms_bar_chart()
    #clean_ms()