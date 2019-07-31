#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 15:40:46 2019

@author: lavanyasingh
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 10:30:59 2019

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
os.chdir('/Users/lavanyasingh/Desktop/GSC2O19internet_archive/')

from prefixes import prefixes
import helpers
import urllib.parse
import csv


q_endpoint = 'http://lavanya-dev.us.archive.org:3030/testwn/query'
u_endpoint = 'http://lavanya-dev.us.archive.org:3030/testwn/update'

endpoint_url = u_endpoint

def get_meta(path):
    pieces = path.split('_')
    return pieces[0]

def get_graph_spec(info):
    url_raw, metasource = info[0], info[1]
    q = ''
    if helpers.is_bad(url_raw): 
        print(url_raw)
        return q
    if url_raw.find('.') == -1: return q
    url = '<http://' + urllib.parse.quote(url_raw) + '>'
    url_item = '<http://' + urllib.parse.quote(url_raw) + '/item>'
    graph = """ GRAPH """ + url 
    ms = helpers.strip_spaces(metasource)
    q = "INSERT {"  + graph + "{" + url_item + "wnp:metasource wni:" + ms + """}}
    WHERE {FILTER (EXISTS {""" + graph + """{?s ?p ?o} } && 
    NOT EXISTS {""" + graph + "{ ?item wnp:metasource wni:" + ms + "}})};"
    return q

#takes in a list of rows
#each row is a string list with one element per cell
def dump_all():
    counter = 0
    q = ''
    sources = get_mc()
    for source in sources:
        s = get_graph_spec(source)
        counter += 1
        q  += s
        if counter % 1000 == 0:
            print(counter)
            query = prefixes + q
            q = ''
            try:
                helpers.send_query(endpoint_url, query)
            except:
                with open('data/logfile', 'w') as f:
                    print('whoops')
                    f.write(query)
                return "yikes"
    print("DONE")
    
def get_mc():
    urls = helpers.read_csv_list('data/mc_sources_meta.csv')
    return [[url, 'mediacloud'] for url in urls]
    

def get_sources():
    sources = []
    pref = '/Users/lavanyasingh/Desktop/GSC2O19internet_archive/data/cleaned'
    paths = os.listdir(pref)
    total = 0
    paths.remove('.DS_Store')
    paths.remove('all.csv')
    for path in paths:
        with open('data/cleaned/' + path, 'r') as inf:
            reader = csv.reader(inf, delimiter=',')
            next(reader)
            for item in reader:
                total += 1
                url = helpers.truncate(item[1])
                if path != 'sheet_cleaned.csv': 
                    meta = get_meta(path)
                else:
                    meta = item[7]
                sources.append([url, meta])
    print("total", total)
    return sources
    
if __name__ == '__main__':
    dump_all()

