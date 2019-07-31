#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 14:36:04 2019

@author: lavanyasingh
"""

import os
os.chdir('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/')
import urllib.parse
import csv
import re
import json
import helpers

class truncator():
    
    def clean_meta(meta):
        return meta.lower().replace(" ", "").strip()
    
    def clean_url(url):
        url_raw = helpers.truncate(url)
        o = urllib.parse.urlparse('http://www.' + url_raw)
        return o.netloc
    
    def prep_url(url):
        url = url.replace("http://", "").replace("https://", "").replace("www.", "")
        return "http://www." + url
    
    def url_is_good(url):
        return (url != "url" and url != "" and url != "www." and url != 'www.source url'
                and url != 'www.www.source url')
    
    def path_is_good(path):
        if (path.find('/robots.txt') != -1 or path.find('html') != -1 or path.find('/css') != -1 
            or path.find('/js') != -1 or path.find('/favicon.ico') != -1 or path.find('/img') != -1 or
            path == '/' or path == "" or path == "/\n" or path.find('.json') != -1 
            or path.find('.js') != -1 or path.find(".png") != -1 or path.find(".jpg") != -1):
            return False
        if len(path.split("/")) > 3: 
            return False
        try:
            int(path.strip().replace("/", ""))
            return False
        except:
            return True
    
    pref = '/Users/lavanyasingh/Desktop/GSC2O19internet_archive/data/raw'
    paths = os.listdir(pref)
    paths.remove(".DS_Store")
    
    #returns a dict 
    def make_path_dict():
        total, uq = 0, 0
        sources = {}
        for path in paths:
            print(path)
            with open('data/raw/' + path, 'r') as inf:
                reader = csv.reader(inf, delimiter=',')
                for line in reader:
                    total += 1
                    line = ''.join(line[1])
                    url = clean_url(line)
                    if url_is_good(url):
                        o = urllib.parse.urlparse(prep_url(line))
                        path = o.path
                        if url not in sources:
                            uq += 1
                            sources.update({url:[]})
                        if path not in sources[url] and path_is_good(path):
                            sources[url].append(path)
                        if total % 10000 == 0 and len(sources[url]) < 15: 
                            print(total, line, url, sources[url])
            print("TOTAL", total)
            print("UNIQUE", uq)
        return sources
    
    #sources = make_path_dict()
    
    def test():
        with open('data/raw/all_Raw.csv', 'r') as inf:
            reader = csv.reader(inf, delimiter=',')
            total = 0
            for line in reader:
                total += 1
                if total % 10000 == 0:
                    print(line[1], clean_url(line[1]))
    
    #outputs a dict of url: CSV rows
    def make_all_data():
        total, uq = 0, 0
        rows = {}
        for path in paths:
            print(path)
            with open('data/raw/' + path, 'r') as inf:
                reader = csv.reader(inf, delimiter=',')
                for line in reader:
                    total += 1
                    url = clean_url(line[1])
                    line[1] = url
                    metasource = clean_meta(line[7])
                    row = line
                    if (row[0] == "United States" or row[0].lower() == "us" or 
                        row[0].lower() == "usa") : 
                        row[0] == "United States of America"
                    row[7] = [metasource]
                    row = [row[i] for i in range(12)] + ['', '']
                    if url not in rows:
                        if url_is_good(url):
                            uq += 1
                            if len(sources[url]) < 10:
                                row[13] = sources[url]
                            else:
                                row[13] = []
                            rows.update({url: row})
                    else:
                        rows[url][7].append(metasource) if metasource not in rows[url][7] else rows[url][7]
                        for i in range(len(rows[url]) - 1):
                            if helpers.is_bad(rows[url][i]):
                                try:
                                    rows[url][i] = row[i] 
                                except:
                                    print(row, i)
                                    return "OOPS"
                    if total % 10000 == 0 and url_is_good(url): 
                        print(url, rows[url])
            print("DONE", path, total, uq)
        return rows
                            
    rows = make_all_data()  
       
    def write_all_data():
        total = 0
        with open('data/raw/all_raw_cleaned.csv', 'w') as outf:
            w = csv.writer(outf, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
            for row in rows.values():
                total += 1
                metasources = ""
                for item in row[7]: 
                    metasources += item + " "
                paths = ""
                for item in row[13]: 
                    paths += item + " "
                row[7] = metasources
                row[13] = paths
                w.writerow(row)
        print("DONE", total)
    
    write_all_data()
        
if __name__ == "__main__":
    truncator = truncator()
    truncator.write_all_data()