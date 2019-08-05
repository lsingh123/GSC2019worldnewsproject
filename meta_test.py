#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 15:49:40 2019

@author: lavanyasingh
"""

# script to determine optimal number of workers for get_meta.py

from meta_scrape import MetadataParser
import timeit
import matplotlib.pyplot as plt


def run_script(processes):
    crawler = MetadataParser(processes)
    time = timeit.timeit(crawler.main, number = 1)
    print(time)
    return time

def time(max_processes):
    times = [run_script(i) for i in range(2, max_processes+1)]
    plt.plot(range(2, max_processes+1), times)
    print("MIN:", min(times), times.index(min(times)))
    plt.ylabel('time')
    plt.xlabel('processes')
    plt.show()

def verify(processes):
    crawler = MetadataParser(processes=processes)
    res = crawler.main()
    count = 0
    for url in res:
        print(url[1])
        if url[1].replace('b', "").find('upstream request timeout') != -1:
            count += 1
    return count

def run_test(max_processes):
    counts = [verify(i) for i in range(2, max_processes+1)]
    plt.plot(range(2, max_processes+1), counts)
    plt.ylabel('request timeouts')
    plt.xlabel('processes')
    plt.show()
    
if __name__ == "__main__":
    run_test(16)
    