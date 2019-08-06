#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 11:20:23 2019

@author: lavanyasingh
"""

import helpers
import csv
import tldextract

# read in common crawl data
def read_cc():
    with open("data/common_crawl.txt", "r") as f:
        sources = set()
        reader = csv.reader(f, delimiter='\t')
        for line in reader:
            sources.add(helpers.truncate(line[1]))
    print("CC", len(sources))
    return sources

# read in old data
def read_all():
    sources = []
    with open("data/raw/all_raw_cleaned.csv", "r") as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            sources.append(line)
    print(len(sources))
    return sources

# remove duplicates
def remove_dups():
    domains = []
    cc_urls = read_cc()
    lines = read_all()
    old_urls = [line[1] for line in lines]
    # make list of old Private Domains (without TLD)
    for item in old_urls:
        url = helpers.clean(item)
        o = tldextract.extract(url)
        domain = o.subdomain + o.domain
        if domain not in domains:
            domains.append(domain)
    for item in cc_urls:
        url = helpers.clean(item)
        o = tldextract.extract(url)
        domain = o.subdomain + o.domain
        # append URL if Private Domain is unique
        if domain not in domains:
            lines.append(["", url, "", "", "", "", "", "commoncrawl",
                              "", "", "", "", ""])
    return lines

def write():
    lines = remove_dups()
    with open("data/all_raw_cleaned1.csv", 'a') as outf:
        w = csv.writer(outf, delimiter=',', quotechar='"', 
                       quoting=csv.QUOTE_MINIMAL)
        for line in lines:
            w.writerow(line)

if __name__ == '__main__':
    write()