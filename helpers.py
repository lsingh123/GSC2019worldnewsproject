#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 10:51:35 2019

@author: lavanyasingh
"""

import re
import os 
import pickle
#from googleapiclient.discovery import build
#from google_auth_oauthlib.flow import InstalledAppFlow
#from google.auth.transport.requests import Request
#from SPARQLWrapper import SPARQLWrapper, JSON
import csv
from prefixes import prefixes
import urllib

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

#CONVENTIONS: 
#CSV ROW has the following columns: ['country', 'url', 'title', 'language', 'type', 
# *'title native language', *'paywall', *'metasource', *'state', *'town', 
#*'wikipedia name', *'redirects?', *'wikipedia link']
#a ROW  (google sheets) is: Title, Title (english not available), URL, Type, Paywall, Source, Language, Country
#TRUNCATED URLS are in the form [*].domain.TLD.[*]
#an entry ISBAD if it is empty, None, NA, or TODO
#SPREADSHEET_ID: test = test sheet, real_deal = the real sheet

#deprecated
def truncate_old(url):
    url = url.strip()
    stream = re.finditer('//', url)
    try:
        url = url[next(stream).span()[1]:]
    except StopIteration:
        url = url
    www = url.find('www.')
    if www != -1:
        url = url[www+4:]
    stream = re.finditer('/', url)
    try:
        url = url[:next(stream).span()[0]]
    except StopIteration:
        url = url
    stream = re.finditer('#', url)
    try:
        url = url[:next(stream).span()[0]]
    except StopIteration:
        url = url
    stream = re.finditer('%', url)
    try:
        url = url[:next(stream).span()[0]]
    except StopIteration:
        url = url
    stream = re.finditer('\?', url)
    try:
        url = url[:next(stream).span()[0]]
    except StopIteration:
        url = url
    stream = re.finditer('\&', url)
    try:
        url = url[:next(stream).span()[0]]
    except StopIteration:
        url = url        
    try:
        int(url.replace('.', ''))
        return ''
    except:
        None
    return url.replace('subject=', '')
    
def truncate(url):
    url = url.replace('%2F', '/').strip()
    stream = re.finditer('//', url)
    try:
        url = url[next(stream).span()[1]:]
    except StopIteration:
        url = url
    www = url.find('www.')
    if www != -1:
        url = url[www+4:]
    if url.find('subject=') != -1:
        return ''
    o = urllib.parse.urlparse('http://www.' + url)
    return o.netloc  

def is_bad(entry):
    if type(entry) == str: entry = entry.strip(' ')
    b = (entry == "TODO" or entry == 'None' or entry == 'none' or entry == '' or 
     entry == 'na' or entry == 'NA' or entry == 'todo' or entry == 'Todo' or entry == [] 
     or entry == "[]" or entry == [''])
    return b

def initialize():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
       with open('token.pickle', 'rb') as token:
           creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
            
    service = build('sheets', 'v4', credentials=creds)
    return service

def send_query(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def get_id(url):
    id = url.split("/")
    return id[len(id)-1]

#returns list of row dictionaries in url:row format (cleans URLS)
#each row is a string list with one element per cell
#also returns total number of rows
def get_sources(spreadsheet_id, service):
    result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range='A:H').execute()
    count = 1
    sources = []
    numRows = result.get('values') if result.get('values')is not None else 0
    for row in numRows:
        count += 1
        try:
            url = truncate(row[2])
            new_row = []
            for i in range(9):
                try: new_row.append(url) if i == 2 else new_row.append(row[i])
                except IndexError: new_row.append("") 
            sources.append({url:new_row})
        except IndexError as e:
            print(count, e)
    return sources, count

#takes list of dicts in url:row format and returns a list of rows
def dict_to_list(d):
    sources = []
    for item in d:
        for url in item:
            sources.append(item[url])
    return sources
        
#reads in a CSV of URLs and returns a list of cleaned and deduped CSV rows (see conventions)
def read_sources(path):
    sources = []
    urls = []
    uq = 0 
    total = 0
    with open(path, 'r', errors = 'ignore') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        for line in reader:
            total += 1 
            url = truncate(line[1])
            print(url)
            if url not in urls:
                uq +=1
                sources.append({'country':line[0], 'url': url, 'title': line[2], 
                               'language': line[3], 'type': line[4]})
                urls.append(url)
    print(path, total, uq)
    return sources

#takes a CSV of URLs and returns a list of cleaned and deduped URLS
def read_csv_list(path):
    sources = []
    total, uq = 0, 0
    with open(path, 'r', errors = 'ignore') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        for line in reader:
            total += 1
            url = truncate(line[1])
            if url not in sources: 
                uq += 1
                sources.append(url)
    print ('total', total)
    print ('unique', uq)
    return sources

#takes a CSV of URLs and returns a list of cleaned and deduped rows
def read_csv_rows(path):
    sources = []
    total, uq = 0, 0
    with open(path, 'r', errors = 'ignore') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        for line in reader:
            total += 1
            row = ['', '', truncate(line[1]), '', '', '', '', '']
            if row not in sources: 
                uq += 1
                sources.append(row)
    print ('total', total)
    print ('unique', uq)
    return sources

#takes a text file of URLs and returns a list of cleaned and deduped URLS
def read_list(path):
    sources = []
    total, uq = 0, 0
    with open(path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            total += 1
            url = truncate(line)
            if url not in sources: 
                print(url)
                uq += 1
                sources.append(url)
    print ('total', total)
    print ('unique', uq)
    return sources

#cleans a string to be loaded in to the database
def clean(s):
    return s.replace("\\", '').replace('\n', '').replace('\'', "'").replace('"', '').replace("'",'').strip()

#removes spaces and makes a string lowercase
def strip_spaces(s):
    return s.replace(' ', '').lower()

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
        codes[strip_spaces(item['itemLabel']['value']).lower()] = get_id(item['item']['value'])
            
    return codes

#reads a CSV of rows and returns a list of rows
def read_in(path):
    sources = []
    with open(path, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        for line in reader:
            sources.append(line)
    return sources

def clean_url(url):
    return url.replace("'", '').replace('"', '').replace('\n', '').replace(' ', '')