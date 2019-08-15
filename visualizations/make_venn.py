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
from matplotlib_venn import venn3
import argparse

class Venn():
    
    def __init__(self, infile="data/all_raw_cleaned.csv", 
                 outfile="visualizations/venn.png"):
        self.infile = infile
        self.outfile = outfile

    #read all sources in from a CSV in {metasource: [source list]} format
    def get_sources(self):
        sources = {"original":[], "mediacloud":[], "wikidata":[]}
        with open(self.infile, "r", errors = "ignore") as f:
            reader = csv.reader(f, delimiter = ",")
            for line in reader:
                metasources = line[7].split(" ")
                for metasource in metasources:
                    try:
                        sources[metasource].append(line[1])
                    except KeyError:
                        pass
        return sources
    
    #make a venn diagram documenting the overlap in URLs for each metasource
    def compare_overlap(self):
        sources = self.get_sources()
        urls, labels = [], []
        for key, value in sources.items():
            urls.append(set(value))
            labels.append(key)
        venn3(urls, labels)
        plt.savefig(self.outfile)
        
# create argument parser
def create_parser():
    argp = argparse.ArgumentParser(
            description='Make a venn diagram of URLs from metasources')
    argp.add_argument('-inf', '--infile', nargs='?',
                      default='data/all_raw_cleaned.csv', type=str,
                      help='csv file to read URLs in from')
    argp.add_argument('-outf', '--outfile', nargs='?',
                      default="visualizations/venn.png", type=str,
                      help='file to write viz to')
    return argp


if __name__=='__main__':
    argp = create_parser()
    args = argp.parse_args()
    venn_maker = Venn(infile=args.infile, outfile=args.outfile)
    venn_maker.compare_overlap()
            