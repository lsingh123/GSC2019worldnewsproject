#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 13:41:18 2019

@author: lavanyasingh
"""

import pandas as pd
import concurrent.futures
import requests
import time
import os
os.chdir(os.path.dirname(os.getcwd()))
import csv

class statusChecker():
    
    CONNECTIONS = 100
    TIMEOUT = 5
    PATH = os.getcwd() + "/data/raw/"
    
    def __init__(self, outfile):
        self.urls = self.read_in()
        self.out = []
        self.outfile = outfile
    
    def read_in(self):
        with open("all_raw_cleaned.csv", 'r') as f:
            reader = csv.reader(f, delimiter=',')
            sources = [("http://" + "".join(line[1])) for line in reader]
        print("DONE READING")
        return sources
        
    def load_url(self, url, timeout):
        try:
            ans = requests.head(url, timeout=timeout, allow_redirects = True)
            redirect = "None"
            if ans.history != []:
                redirect = ans.url
            return url, ans.status_code, redirect
        except Exception:
            return url, "ERROR"
    
    def write_codes(self, codes):
        with open(self. outfile, 'w') as outf:
            w = csv.writer(outf, delimiter= ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
            for url in codes:
                w.writerow([url])
        print("WROTE ALL CODES")
    
    def get_data(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.CONNECTIONS) as executor:
            future_to_url = (executor.submit(self.load_url, url, self.TIMEOUT) for url in self.urls)
            time1 = time.time()
            for future in concurrent.futures.as_completed(future_to_url):
                self.out.append(future.result())
                print(str(len(self.out)),end="\r")
            time2 = time.time()
            return time1, time2
        
    def main(self):
        time1, time2 = self.get_data()
        print(f'Took {time2-time1:.2f} s')
        self.write_codes(self.out)

if __name__ == "__main__":
    statusChecker = statusChecker("codes.csv")
    statusChecker.main()


