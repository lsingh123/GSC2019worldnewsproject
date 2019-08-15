#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 10:51:35 2019

@author: lavanyasingh
"""

import re
from SPARQLWrapper import SPARQLWrapper, JSON
import csv
from prefixes import prefixes
import urllib

#CONVENTIONS: 
#CSV ROW has the following columns: ['country', 'url', 'title', 'language', 'type', 
# *'title native language', *'paywall', *'metasource', *'state', *'town', 
#*'wikipedia name', *'redirects?', *'wikipedia link']
#a ROW  (google sheets) is: Title, Title (english not available), URL, Type, Paywall, Source, Language, Country
#TRUNCATED URLS are in the form [*].domain.TLD.[*]

# clean a url to be truncated or for domain extraction
def clean_url(url):
    url = url.replace("www.", "")
    url = url.strip(".").strip("/")
    stream = re.finditer('%', url)
    try:
        url = url[:next(stream).span()[0]]
    except StopIteration:
        url = url
    return url

# truncate a URL to its host name
def truncate(url):
    url = url.replace('%2F', '/').strip()
    stream = re.finditer('//', url)
    try:
        url = url[next(stream).span()[1]:]
    except StopIteration:
        url = url
    if url.find('subject=') != -1:
        return ''
    url = clean_url(url)
    o = urllib.parse.urlparse('http://www.' + url)
    return o.netloc  

#cleans a string to be loaded in to the database
def clean_string(s):
    return (s.replace("\\", '').replace('\n', '').replace('\'', "'").
            replace('"', '').replace("'",'').strip())

#removes spaces and makes a string lowercase
def strip_spaces(s):
    return s.replace(' ', '').lower()

# return True if entry is bad false otherwise
def is_bad(entry):
    if type(entry) == str: entry = entry.strip(' ')
    b = (entry == "TODO" or entry == 'None' or entry == 'none' or entry == '' 
         or entry == 'na' or entry == 'NA' or entry == 'todo' or 
         entry == 'Todo' or entry == [] or entry == "[]" or entry == [''])
    return b

#takes list of dicts in url:row format and returns a list of rows
def dict_to_list(d):
    sources = []
    for item in d:
        for url in item:
            sources.append(item[url])
    return sources

# gets wikidata country_id from country url
def get_id(url):
    id = url.split("/")
    return id[len(id)-1]

#returns a dict of country:country codes
def get_countries():
    endpoint_url = "https://query.wikidata.org/sparql"
    query = prefixes + """
    SELECT ?item ?itemLabel
    WHERE 
    {
      {?item wdt:P31 wd:Q6256} UNION
      {?item wdt:P31 wd:Q3624078} UNION
      {?item wdt:P31 wd:Q33837} UNION
      {?item wdt:P31 wd:Q27561} UNION
      {?item wdt:P31 wd:Q82794}.
      SERVICE wikibase:label  { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    } """
    cResults = send_query(endpoint_url, query)
    cRes = cResults['results']['bindings']
    codes = {}
    for item in cRes:
        country = strip_spaces(item['itemLabel']['value']).lower()
        codes[country] = get_id(item['item']['value'])
    return codes

# send a SPARQL query to a given endpoint
def send_query(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

#reads a CSV of rows and returns a list of rows
def read_in(path):
    sources = []
    with open(path, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        for line in reader:
            sources.append(line)
    return sources