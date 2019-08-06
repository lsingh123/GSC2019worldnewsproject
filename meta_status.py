#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 13:41:18 2019

@author: lavanyasingh
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import time
import csv
import argparse

class statusChecker():
    
    CONNECTIONS = 100
    TIMEOUT = 50
    
    def __init__(self, infile='data/all_raw_cleaned.csv', 
                 outfile='data/codes2.csv'):
        self.out = []
        self.outfile, self.infile = outfile, infile
        self.urls = self.read_in()
    
    def read_in(self):
        with open(self.infile, 'r') as f:
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
            w = csv.writer(outf, delimiter= ',', quotechar = '"', 
                           quoting = csv.QUOTE_MINIMAL)
            for url in codes:
                w.writerow(list(url))
        print("WROTE ALL CODES")
    
    def main(self):
        with ThreadPoolExecutor(max_workers=self.CONNECTIONS) as executor:
            future_to_url = (executor.submit(self.load_url, url, self.TIMEOUT) 
                            for url in self.urls)
            time1 = time.time()
            for future in as_completed(future_to_url):
                self.out.append(future.result())
                print(str(len(self.out)),end="\r")
            time2 = time.time()
        self.write_codes(self.out)
        print(f'Took {time2-time1:.2f} s')

# create argument parser
def create_parser():
    argp = argparse.ArgumentParser(
            description='check status codes')
    argp.add_argument('-inf', '--infile', nargs='?',
                      default='data/all_raw_cleaned.csv', type=str,
                      help='csv file to read URLs in from')
    argp.add_argument('-outf', '--outfile', nargs='?',
                      default='data/codes2.csv', type=str,
                      help='csv file to write codes to')
    return argp

if __name__ == "__main__":
    argp = create_parser()
    args = argp.parse_args()
    statusChecker = statusChecker(infile=args.infile, outfile=args.outfile)
    statusChecker.main()


