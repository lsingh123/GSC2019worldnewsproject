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
import helpers

class truncator():
    
    # cleans metasource name
    def clean_meta(selfm, meta):
        return meta.lower().replace(" ", "").strip()
    
    def clean_url(self, url):
        url_raw = helpers.truncate(url)
        o = urllib.parse.urlparse('http://www.' + url_raw)
        return o.netloc
    
    # strip schema and www. from a given URL
    def prep_url(self, url):
        url = (url.replace("http://", "").replace("https://", "")
        .replace("www.", ""))
        return "http://www." + url
    
    def url_is_good(self, url):
        # garbage URLs as determined by spotchecking
        return (url != "url" and url != "" and url != "www." and 
                url != 'www.source url' and url != 'www.www.source url')
    
    def path_is_good(self, path):
        # we want to exclude generic paths
        bad = ['/robots.txt', 'html', '/css', '/js', '/favicon.ico', '/img', 
               '.json', '.js', ".png", ".jpg"]
        for el in bad:
            if path.find(el) != -1: return False
            
        # we want to exclude empty paths
        if (path == '/' or path == "" or path == "/\n"):
            return False
        
        # we want to exclude long paths
        if len(path.split("/")) > 3: 
            return False
        
        # we want to exclude paths that are purely numerical
        try:
            int(path.strip().replace("/", ""))
            return False
        except:
            return True
    
    # returns a dict of url: paths when given a list of filepaths
    # example return value: {'cnn': '/money', '/business', '/politics'}
    def make_path_dict(self, fpaths):
        sources = {}
        for fpath in fpaths:
            with open('data/raw/' + fpath, 'r') as inf:
                reader = csv.reader(inf, delimiter=',')
                for line in reader:
                    line = ''.join(line[1])
                    url = self.clean_url(line)
                    
                    # ignore bad URLs
                    if not self.url_is_good(url):
                        pass

                    o = urllib.parse.urlparse(self.prep_url(line))
                    path = o.path
                    
                    # add unique URLs
                    if url not in sources:
                        sources.update({url:[]})
                    
                    # if we've seen this URL before, add path
                    elif (path not in sources[url] and 
                          self.path_is_good(path)):
                        sources[url].append(path)
        return sources
        
    #outputs a dict of url: CSV rows
    def make_all_data(self, fpaths):
        rows = {}
        for fpath in fpaths:
            with open('data/raw/' + fpath, 'r') as inf:
                reader = csv.reader(inf, delimiter=',')
                for line in reader:
                    url = self.clean_url(line[1])
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