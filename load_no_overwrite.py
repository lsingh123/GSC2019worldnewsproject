#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 11:28:34 2019

@author: lavanyasingh
"""

from prefixes import prefixes
import helpers
import urllib.parse

class Feeder:
    
    ENDPOINT = 'http://lavanya-dev.us.archive.org:3030/testwn/update'
    
    def __init__(self):
        self.countries = helpers.get_countries()
    
    # takes a raw country name and returns wikidata country code if it exists
    def get_country_code(self, name):
        try:
            return 'wd:'+ self.countries[helpers.strip_spaces(name).lower()]
        except KeyError as e:
            return("\'TODO\'")
            print(e)
    
    def get_graph_spec(self, source):
        q = ''
        if helpers.is_bad(source[1]): 
            print(source[1])
            return q
        # this means our url is not valid
        if source[1].find('.') == -1: return q
        
        # begin constructing graph spec
        # construct item
        item = '<http://' + urllib.parse.quote(source[1]) + '/item>' 
        # construct item URL
        url = '<http://' + urllib.parse.quote(source[1]) + '>'
        # construct graph value
        graph = """ GRAPH """ + url 
        
        # add URL
        q += ("INSERT { " + graph + " {" + item + " wdt:P1896 \'" + 
                urllib.parse.quote(source[1]) + """\' }} 
                WHERE {FILTER (NOT EXISTS {""" + graph + 
                "{ ?item wdt:P1896 ?url}})} ;" )
        
        # add country
        if not helpers.is_bad(source[0]):
            country_code = self.get_country_code(source[0])
            if not helpers.is_bad(country_code):
                c = country_code
            else:
                c = helpers.clean(source[0])
            q += (" INSERT { " + graph + " {" + item + " wdt:P17 \'" + c 
                    + """\' }}
            WHERE {FILTER (NOT EXISTS {""" + graph + 
            "{ ?item wdt:P17 ?country}})} ;" )
            
        # add title title
        if not helpers.is_bad(source[2]):
            q += (" INSERT { " + graph + " {" + item + " wdt:P1448 \'" + 
                                            helpers.clean(source[2]) + """\' }}
            WHERE {FILTER (NOT EXISTS {""" + graph + 
            "{ ?item wdt:P1448 ?title}})} ;" )

        # add language
        if not helpers.is_bad(source[3]):
            q += (" INSERT { " + graph + " {" + item + " wdt:P37 \'" + 
                                            helpers.clean(source[3]) + """\' }}
            WHERE {FILTER (NOT EXISTS {""" + graph 
                                       + "{ ?item wdt:P37 ?lang}})} ;" )

        # add source type
        if not helpers.is_bad(source[4]):
            q += (" INSERT { " + graph + " {" + item + " wdt:P31 \'" + 
                                            helpers.clean(source[4]) + """\' }}
            WHERE {FILTER (NOT EXISTS {""" + graph 
                                       + "{ ?item wdt:P31 ?type}})} ;" )

        # add title in native language
        if not helpers.is_bad(source[5]):
            q += (" INSERT { " + graph + " {" + item + " wdt:P1704 \'" + 
                                            helpers.clean(source[5]) + """\' }}
            WHERE {FILTER (NOT EXISTS {""" + graph 
                                    + "{ ?item wdt:P1448 ?title_native}})} ;" )

        # add paywall (Yes or No)
        if not helpers.is_bad(source[6]):
            q += (" INSERT { " + graph + " {" + item + " wnp:paywalled \'" + 
                                            helpers.clean(source[6]) + """\' }}
            WHERE {FILTER (NOT EXISTS {""" + graph 
                                       + "{ ?item wnp:paywalled ?pw}})} ;" )

        # add metasource
        if not helpers.is_bad(source[7]):
            q += (" INSERT { " + graph + " {" + item + " wnp:metasource wni:" + 
            helpers.strip_spaces(source[7]).lower()   + """ }}
            WHERE {FILTER (NOT EXISTS {""" + graph 
                                       + "{ ?item wnp:metasource ?ms}})} ;" )

        # add state
        if not helpers.is_bad(source[8]):
            q += (" INSERT { " + graph + " {" + item + " wdt:P131 \'" + 
                                            helpers.clean(source[8]) + """\' }}
            WHERE {FILTER (NOT EXISTS {""" + graph 
                                       + "{ ?item wdt:P131 ?state}})} ;" )
            
        # add wikipedia name
        if not helpers.is_bad(source[10]):
            q += (" INSERT { " + graph + " {" + item + 
                                            " wnp:wikipedia-name \'" + 
                                        helpers.clean(source[10]) + """\' }}
            WHERE {FILTER (NOT EXISTS {""" + graph 
                                + "{ ?item wnp:wikipedia-name ?wp_name}})} ;" )
            
        # add redirect 
        if not helpers.is_bad(source[11]):
            q += (" INSERT { " + graph + " {" + item + " wnp:redirect \'" + 
                                    helpers.clean(source[11]) + """\' }}
            WHERE {FILTER (NOT EXISTS {""" + graph 
                                       + "{ ?item wnp:redirect ?rd}})} ;" )
            
        # add wikipedia link
        if not helpers.is_bad(source[12]):
            q += (" INSERT { " + graph + " {" + item + " wnp:wikipedia-page \'" 
                                        + helpers.clean(source[12]) + """\' }}
            WHERE {FILTER (NOT EXISTS {""" + graph 
                                + "{ ?item wnp:wikipedia-page ?wp_page}})} ;" )
        
        return q

    # takes in a list of CSV Rows
    # each row is a string list with one element per cell
    def dump_all(self, sources):
        counter = 0
        q = ''
        for source in sources:
            s = self.get_graph_spec(source)
            counter += 1
            q  += s
            if counter % 1000 == 0:
                print(str(counter) + "\r")
                query = prefixes + q
                q = ''
                # breaks at a bad query and writes it to logfile
                try:
                    helpers.send_query(self.ENDPOINT, query)
                except:
                    with open('data/logfile.log', 'w') as f:
                        f.write(query)
                        break
        print("DONE")

if __name__ == '__main__':
    feeder = Feeder()
    feeder.dump_all(helpers.read_in(infile))
    
   
