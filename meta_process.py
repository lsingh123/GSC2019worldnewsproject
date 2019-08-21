#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 10:01:49 2019

@author: lavanyasingh
"""

# a script to clean the results of meta_scrape.py and retry failed links

import csv
from meta_scrape import MetadataParser
import sys
from helpers import is_bad
from fuzzywuzzy import process


def clean_meta(infile='data/metadata.csv', outfile='data/metadata_cleaned.csv'):
    bad = []
    total = 0
    csv.field_size_limit(sys.maxsize)
    parser = MetadataParser(in_urls=[])
    with open(infile, "r", errors = "ignore") as inf, open(outfile, 'w') as outf:
        reader = csv.reader(inf, delimiter = ",")
        w = csv.writer(outf, delimiter= ',', quotechar = '"', 
                           quoting = csv.QUOTE_MINIMAL)
        for line in reader:
            total += 1
            if len(line) > 3:
                w.writerow(line)
            elif (str(line[1]).find("upstream request timeout") != -1 or 
                  str(line[1]).find("HTTP Connection Pool") != -1):
                bad.append(line[0])
            elif str(line[1]).find("html") != -1:
                line = parser.parse_url(line[0], html=str(line[1]))
                w.writerow(line)
            print(str(total), end = "\r")
    print("DONE PARSING {total} URLs".format(total=total))
    return bad

def fix_bad():
    bad = clean_meta()
    parser = MetadataParser(in_urls=bad, outfile="data/metadata_cleaned.csv",
                            retries=3)
    parser.main()
    
def read_meta(infile='data/metadata_cleaned.csv'):
    good = {}
    total = 0
    csv.field_size_limit(sys.maxsize)
    with open(infile, "r", errors = "ignore") as inf:
        reader = csv.reader(inf, delimiter = ",")
        for line in reader:
            total += 1
            if len(line) > 3:
                url = line[0].replace("http://", "").replace("https://", "")
                good.update({url:line})
    print("DONE PARSING {total} URLs".format(total=total))
    return good

def consolidate(infile="data/all_raw_cleaned.csv", outfile="data/all_metadata.csv"):
    good = read_meta()
    total = 0
    with open(infile, "r", errors = "ignore") as inf, open(outfile, 'w') as outf:
        reader = csv.reader(inf, delimiter = ",")
        w = csv.writer(outf, delimiter= ',', quotechar = '"', 
                           quoting = csv.QUOTE_MINIMAL)
        for line in reader:
            total += 1
            while len(line) < 16:
                line.append("")
                
            url = line[1].replace("www.", "")
            if url in good:
                
                # add title if not there
                if not is_bad(good[url][1]) and is_bad(line[2]):
                    line[2] = good[url][1]
                
                # add description
                if not is_bad(good[url][2]):
                    line[14] = good[url][2]
                
                # add locale
                if not is_bad(good[url][3]):
                    line[15] = good[url][3]
        
            w.writerow(line)
            print(str(total), end = "\r")


def get_codes(cfile="data/countries_iso.csv", lfile="data/languages.csv"):
    countries = {}
    with open(cfile, "r", errors = "ignore") as inf:
        reader = csv.reader(inf, delimiter = ",")
        for line in reader:
            countries.update({line[1]:line[0], line[2]:line[0]})
    print("countries")
    languages = {}
    with open(lfile, "r", errors = "ignore") as inf:
        reader = csv.reader(inf, delimiter = ",")
        for line in reader:
            languages.update({line[1]:line[2], line[0]:line[2]})
    print("languages")
    return countries, languages

countries, languages = get_codes()

def parse_country(code):
    p = process.extractOne(code, list(countries.keys()))
    if p[1] > 87:
        code = p[0]
        return countries[code]
    return None

def parse_lang(code):
    p = process.extractOne(code, list(languages.keys()))
    if p[1] > 87:
        code = p[0]
        return languages[code]
    return None

def parse_locale(locale):
    try:
        [l_code, c_code] = locale.split("_") 
        
        return parse_country(c_code), parse_lang(l_code)
    except ValueError:
        val = parse_country(locale)
        if val is None:
            val = parse_lang(locale)
        return val, val
                    
def locale_to_country(infile="data/all_metadata.csv", outfile="data/all_metadata2.csv"):
    total = 0
    with open(infile, "r", errors = "ignore") as inf, open(outfile, 'w') as outf:
        reader = csv.reader(inf, delimiter = ",")
        w = csv.writer(outf, delimiter= ',', quotechar = '"', 
                           quoting = csv.QUOTE_MINIMAL)
        
        for line in reader:
            total += 1
            
            if not is_bad(line[15]):

                country, language = parse_locale(line[15])
                
                if language != line[3] and not is_bad(language):
                    line[3] = language
                
                if country != line[0] and not is_bad(country):
                    line[0] = country 
            
            w.writerow(line)
            print(str(total), end = "\r")

if __name__ == '__main__':
     consolidate()
     locale_to_country()
    