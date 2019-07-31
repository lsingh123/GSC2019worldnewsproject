#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 15:37:51 2019

@author: lavanyasingh
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 11:28:34 2019

@author: lavanyasingh
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 12:49:40 2019

@author: lavanyasingh
"""


import os
os.chdir('/Users/lavanyasingh/Desktop/oldGSC/')

from prefixes import prefixes
import helpers
import urllib.parse
import json
import csv

q_endpoint = 'http://lavanya-dev.us.archive.org:3030/testwn/query'
u_endpoint = 'http://lavanya-dev.us.archive.org:3030/testwn/update'

endpoint_url = u_endpoint

def write_meta_sources():
    query = prefixes + """
    INSERT DATA {
    GRAPH <http://worldnews/metasources> {
        wni:mediacloud wdt:P1448 "MediaCloud".
        wni:datastreamer wdt:P1448 "DataStreamer".
        wni:original wdt:P1448 "Original".
        wni:inkdrop wdt:P1448 "InkDrop".
        wni:wikidata wdt:P1448 "WikiData".
        wni:wikipedia wdt:P1448 "Wikipedia".
        wni:abyz wdt:P1448 "ABYZNewsLinks".
        wni:onlineradiobox wdt:P1448 "OnlineRadioBox".
        wni:w3newspapers wdt:P1448 "W3Newspapers".
        wni:newscrawls wdt:P1448 "Newscrawls".
        wni:topnews wdt:P1448 "Top_News".
        wni:gdelt wdt:P1448 "GDELT".
        wni:newsgrabber wdt:P1448 "Newsgrabber".
        wni:wikinews wdt:P1448 "Wikinews".
        wni:usnpl wdt:P1448 "USNPL".
        wni:dmoz wdt:P1448 "DMOZ".
        wni:prensaescrita wdt:P1448 "Prensa Escrita".}
    } """
    helpers.send_query(endpoint_url, query)
    print('successfully wrote meta sources')

countries = helpers.get_countries()

#takes a raw country name and returns wikidata country code if it exists
def get_country_code(name):
    try:
        return 'wd:'+ countries[helpers.strip_spaces(name).lower()]
    except KeyError as e:
        return("\'TODO\'")
        print(e)

def get_ms_spec(metasources):
    q = ''
    for ms in metasources:
        q += """;
            wnp:metasource wni:""" + helpers.strip_spaces(ms).lower() 
    return q

def get_path_spec(paths):
    q = ''
    for path in paths:
        q += """;
            wnp:haspath \'""" + helpers.clean(path) + "\'"
    return q

def get_graph_spec(source):
    if helpers.is_bad(source[1]): 
        print(source[1])
        return ''
    if source[1].find('.') == -1: return ''
    url = '<http://' + urllib.parse.quote(source[1]) + '>'
    url_item = '<http://' + urllib.parse.quote(source[1]) + '/item>' 
    q = """GRAPH """ + url + """ { 
    """ + url_item + """ wdt:P1896 \'""" + urllib.parse.quote(source[1]) + """\'"""
    #country
    if not helpers.is_bad(source[0]):
        country_code = get_country_code(source[0])
        if not helpers.is_bad(country_code):
            q += """;
            wdt:P17 """ + country_code + """ """
        else:
            q += """;
            wdt:P17 \'""" + helpers.clean(source[0]) + """\' """
    #title
    if not helpers.is_bad(source[2]):
        q += """;
            wdt:P1448 \'""" + helpers.clean(source[2]) + """\' """
    #language
    if not helpers.is_bad(source[3]):
        q += """;
            wdt:P37 \'""" + helpers.clean(source[3]) + """\' """
    #type
    if not helpers.is_bad(source[4]):
        q += """;
            wdt:P31 \'""" + helpers.clean(source[4]) + """\' """
    #title (native language)
    if not helpers.is_bad(source[5]):
        q += """;
            wdt:P1704 \'""" + helpers.clean(source[5]) + """\' """    
    #paywall
    if not helpers.is_bad(source[6]):
        q += """;
            wnp:paywalled \'""" + helpers.clean(source[6]) + """\' """
    #metasources
    if not helpers.is_bad(source[7]):
        q += get_ms_spec(source[7])
    #state
    if not helpers.is_bad(source[8]):
        q += """;
            wdt:P131 \'""" + helpers.clean(source[8]) + """\' """
    #town
    if not helpers.is_bad(source[9]):
        q += """;
            wdt:P131 \'""" + helpers.clean(source[9]) + """\' """
    #wikipedia name
    if not helpers.is_bad(source[10]):
        q += """;
            wnp:wikipedia-name \'""" + helpers.clean(source[10]) + """\' """
    #redirects?
    if not helpers.is_bad(source[11]):
        q += """;
            wnp:redirect \'""" + helpers.clean(source[11]) + """\' """
    #wikipedia link
    if not helpers.is_bad(source[12]):
        q += """;
            wnp:wikipedia-page \'""" + urllib.parse.quote(source[12]) + """\'"""
    #paths
    if not helpers.is_bad(source[13]):
        q += get_path_spec(source[13])
    q += """.}
        """  
    return q


#takes in a list of CSV rows
def dump_all(sources):
    counter = 0
    q = ''
    for source in sources:
        s = get_graph_spec(source)
        counter += 1
        q  += s
        if counter % 1000 == 0:
            print(counter)
            query = prefixes + """
            INSERT DATA {
            """ + q + """} """
            q = ''
            try:
                helpers.send_query(endpoint_url, query)
            except:
                with open('data/logfile', 'w') as f:
                    f.write(query)
                return "yikes"
            with open('data/logfile', 'w') as f:
                f.write(query)
    print("DONE")

def read_in():
    sources = []
    total = 0
    with open("data/raw/all_raw_cleaned.csv", 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            total += 1
            line[7] = line[7].strip(" ").split(" ")
            line[13] = line[13].strip(" ").split(" ")
            sources.append(line)
            if total % 10000 == 0: 
                print(total)
    print("DONE", total)
    return sources

if __name__ == '__main__':
    sources = read_in()
    dump_all(sources)
    #s = '["/"divyamarathi.bhaskar.com"]'
    #print(json.loads(s.replace("/", "\\")))


