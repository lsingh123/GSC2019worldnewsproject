#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 14:36:04 2019

@author: lavanyasingh
"""

import urllib.parse
import csv
import helpers

class Truncator():
    
    def __init__(self, outfile="data/all_raw_cleaned2.csv"):
        self.outfile = outfile
    
    def clean_meta(self, meta):
        # cleans metasource name
        return meta.lower().replace(" ", "").strip()
    
    def prep_url(self, url):
        # strip schema and www. from a given URL
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
        
    #outputs a dict of url: CSV rows
    def make_all_data(self, infile):
        rows = {}
        with open('data/' + infile, 'r') as inf:
                reader = csv.reader(inf, delimiter=',')
                for line in reader:

                    # clean URL
                    url = helpers.truncate(line[1])
                    line[1] = url
                    if len(rows) % 5000 == 0: print(url)

                    
                    # get path ('/money' or '/index' for example)
                    o = urllib.parse.urlparse(self.prep_url(line[1]))
                    path = o.path
                    
                    # add metasource
                    metasource = self.clean_meta(line[7])
                    line[7] = [metasource]

                    
                    # check for various spellings of USA
                    if (line[0] == "United States" or line[0].lower() == "us" 
                        or line[0].lower() == "usa") : 
                        line[0] == "United States of America"
                    
                    # extend row
                    line += ['', '']
                    
                    # if unique url, add path
                    if url not in rows:
                        if self.url_is_good(url):
                            if self.path_is_good(path):
                                line[13] = [path]
                            rows.update({url: line})
                    else:
                        # add metasource if necessary
                        if metasource not in rows[url][7]:
                            rows[url][7].append(metasource)
                        
                        # update any broken metadata to new value
                        for i in range(len(rows[url]) - 1):
                            if helpers.is_bad(rows[url][i]):
                                try:
                                    rows[url][i] = line[i] 
                                except:
                                    pass
                        
                        # add path if good
                        if self.path_is_good(path):
                            rows[url][13].append(path)
                            
        return rows
                                   
    def write_all_data(self, rows):
        with open(self.outfile, 'w') as outf:
            w = csv.writer(outf, delimiter= ',', quotechar = '"', 
                           quoting = csv.QUOTE_MINIMAL)
            for row in rows.values():
                metasources = ""
                for item in row[7]: 
                    metasources += item + " "
                paths = ""
                for item in row[13]: 
                    paths += item + " "
                row[7] = metasources
                row[13] = paths
                w.writerow(row)
        print("DONE WRITING")
    
        
if __name__ == "__main__":
    truncator = Truncator()
    rows = truncator.make_all_data("all_raw.csv")
    truncator.write_all_data(rows)