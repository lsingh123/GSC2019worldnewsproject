#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 16:00:58 2019

@author: lavanyasingh
"""

import helpers
import urllib.parse

class graphGenerator():
    
    def __init__(self):
        self.countries = helpers.get_countries()
    
     # takes a raw country name and returns wikidata country code if it exists
    def get_country_code(self, name):
        try:
            return 'wd:'+ self.countries[helpers.strip_spaces(name).lower()]
        except KeyError as e:
            return("\'TODO\'")
            print(e)
    
    # returns a triple for each path given ('/index' for example)
    def get_path_spec(self, paths):
        q = ''
        for path in paths:
            q += """;
                wnp:haspath \'""" + helpers.clean_string(path) + "\'"
        return q

    # returns a triple for each metasource given
    def get_ms(self, metasources):
        q = ''
        for ms in metasources:
            q += """;
                wnp:metasource wni:""" + helpers.strip_spaces(ms).lower() 
        return q
    
    # returns graph spec for overwriting
    def overwrite(self, source):
        q = ''
        
        # check for a valid url
        if helpers.is_bad(source[1]) or source[1].find('.') == -1: 
            return q
        
        # add url to graph
        url = '<http://' + urllib.parse.quote(source[1]) + '>'
        url_item = '<http://' + urllib.parse.quote(source[1]) + '/item>' 
        graph = """ GRAPH """ + url 
    
        # add url
        match = "{" + graph + "{ ?item wdt:P1896 ?url}}"
        q += ("DELETE" + match + """
              INSERT { """ + graph + " {" + url_item + " wdt:P1896 """ 
                                        + url + """ }} 
              WHERE """ + match + ";" )
        
        # add country
        if not helpers.is_bad(source[0]):
            country_code = self.get_country_code(source[0])
            if not helpers.is_bad(country_code):
                c = country_code
            else:
                c = helpers.clean(source[0])
            match = "{" + graph + "{ ?item wdt:P17 ?country}}"
            q += ("DELETE" + match + """
              INSERT { """ + graph + " {" + url_item + " wdt:P17 " + c + """ }} 
              WHERE """ + match + ";" )

        # add title
        if not helpers.is_bad(source[2]):
            match = "{" + graph + "{ ?item wdt:P1448 ?title}}"
            q += ("DELETE" + match + """
              INSERT { """ + graph + " {" + url_item + " wdt:P1448 \'" 
                                        + helpers.clean(source[2]) + """\' }} 
              WHERE """ + match + ";" )

        # add language
        if not helpers.is_bad(source[3]):
            match = "{" + graph + "{ ?item wdt:P37 ?lang}}"
            q += ("DELETE" + match + """
              INSERT { """ + graph + " {" + url_item + " wdt:P37 \'" 
                                        + helpers.clean(source[3]) + """\' }} 
              WHERE """ + match + ";" )

        # add type
        if not helpers.is_bad(source[4]):
            match = "{" + graph + "{ ?item wdt:P31 ?type}}"
            q += ("DELETE" + match + """
              INSERT { """ + graph + " {" + url_item + " wdt:P31 \'" 
                                        + helpers.clean(source[4]) + """\' }} 
              WHERE """ + match + ";" )

        # add title (native language)
        if not helpers.is_bad(source[5]):
            match = "{" + graph + "{ ?item wdt:P1704 ?title}}"
            q += ("DELETE" + match + """
              INSERT { """ + graph + " {" + url_item + " wdt:P1704 \'" + helpers.clean(source[5]) + """\'}} 
              WHERE """ + match + ";" )

        # add paywall
        if not helpers.is_bad(source[6]):
            match = "{" + graph + "{ ?item wnp:paywalled ?pw}}"
            q += ("DELETE" + match + """
              INSERT { """ + graph + " {" + url_item + " wnp:paywalled \'" 
                                        + helpers.clean(source[2]) + """\' }} 
              WHERE """ + match + ";" )

        # add metasource
        if not helpers.is_bad(source[7]):
            match = "{" + graph + "{ ?item wnp:metasource ?ms}}"
            q += ("DELETE" + match + """
              INSERT { """ + graph + " {" + url_item + " wnp:metasource wni:" + 
              helpers.strip_spaces(source[7]).lower() + """ }} 
              WHERE """ + match + ";" )

        # add state
        if not helpers.is_bad(source[8]):
            match = "{" + graph + "{ ?item wdt:P131 ?state}}"
            q += ("DELETE" + match + """
              INSERT { """ + graph + " {" + url_item + " wdt:P131 \'" 
                                        + helpers.clean(source[8]) + """\' }} 
              WHERE """ + match + ";" )

        # add wikipedia name
        if not helpers.is_bad(source[10]):
            match = "{" + graph + "{ ?item wnp:wikipedia-name ?wp_name}}"
            q += ("DELETE" + match + """
              INSERT { """ + graph + " {" + url_item + " wnp:wikipedia-name \'" 
                                        + helpers.clean(source[10]) + """\' }} 
              WHERE """ + match + ";" )

        # add redirects?
        if not helpers.is_bad(source[11]):
            match = "{" + graph + "{ ?item wnp:redirect ?rd}}"
            q += ("DELETE" + match + """
              INSERT { """ + graph + " {" + url_item + " wnp:redirect \'" 
                                        + helpers.clean(source[11]) + """\' }} 
              WHERE """ + match + ";" )

        # add wikipedia link
        if not helpers.is_bad(source[12]):
            match = "{" + graph + "{ ?item wnp:wikipedia-page ?wp_page}}"
            q += ("DELETE" + match + """
              INSERT { """ + graph + " {" + url_item + " wnp:wikipedia-page \'" 
                                        + helpers.clean(source[12]) + """\' }} 
              WHERE """ + match + ";" )
            
        # add description
        if not helpers.is_bad(source[14]):
            match = "{" + graph + "{ ?item wnp:description ?desc}}"
            q += ("DELETE" + match + """
              INSERT { """ + graph + " {" + url_item + " wnp:description \'" 
                                        + helpers.clean(source[14]) + """\' }} 
              WHERE """ + match + ";" )
        
        return q
    
    def no_overwrite(self, source):
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
        q += ("INSERT { " + graph + " {" + item + " wdt:P1896 " + url + """ }} 
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
        
        # add description
        if not helpers.is_bad(source[14]):
            q += (" INSERT { " + graph + " {" + item + " wnp:description \'" 
                                        + helpers.clean(source[14]) + """\' }}
            WHERE {FILTER (NOT EXISTS {""" + graph 
                                + "{ ?item wnp:description ?desc}})} ;" )
        
        return q

    # takes in a CSV row as source
    def first_load(self, source):
        
        # checks for bad URLs
        if helpers.is_bad(source[1]) or source[1].find('.') == -1: 
            return ''
        
        # insert URL
        url = '<http://' + urllib.parse.quote(source[1]) + '>'
        url_item = '<http://' + urllib.parse.quote(source[1]) + '/item>' 
        q = """GRAPH """ + url + """ { 
        """ + url_item + """ wdt:P1896 """ + url
        
        # add country
        if not helpers.is_bad(source[0]):
            country_code = self.get_country_code(source[0])
            if not helpers.is_bad(country_code):
                q += """;
                wdt:P17 """ + country_code + """ """
            else:
                q += """;
                wdt:P17 \'""" + helpers.clean_string(source[0]) + """\' """
            
        # add title
        if not helpers.is_bad(source[2]):
            q += """;
                wdt:P1448 \'""" + helpers.clean_string(source[2]) + """\' """

        # add language
        if not helpers.is_bad(source[3]):
            q += """;
                wdt:P37 \'""" + helpers.clean_string(source[3]) + """\' """

        #add type
        if not helpers.is_bad(source[4]):
            q += """;
                wdt:P31 \'""" + helpers.clean_string(source[4]) + """\' """

        #add title (native language)
        if not helpers.is_bad(source[5]):
            q += """;
                wdt:P1704 \'""" + helpers.clean_string(source[5]) + """\' """    

        # add paywall
        if not helpers.is_bad(source[6]):
            q += """;
                wnp:paywalled \'""" + helpers.clean_string(source[6]) + """\' """

        # add metasources
        if not helpers.is_bad(source[7]):
            q += self.get_ms(source[7])

        # add state
        if not helpers.is_bad(source[8]):
            q += """;
                wdt:P131 \'""" + helpers.clean_string(source[8]) + """\' """

        # add town
        if not helpers.is_bad(source[9]):
            q += """;
                wdt:P131 \'""" + helpers.clean_string(source[9]) + """\' """

        # add wikipedia name
        if not helpers.is_bad(source[10]):
            q += """;
                wnp:wikipedia-name \'""" + helpers.clean_string(source[10]) + "\' "

        # add redirects?
        if not helpers.is_bad(source[11]):
            q += """;
                wnp:redirect \'""" + helpers.clean_string(source[11]) + """\' """

        # add wikipedia link
        if not helpers.is_bad(source[12]):
            q += """;
                wnp:wikipedia-page \'""" + urllib.parse.quote(source[12]) + """\'"""

        # add paths
        if not helpers.is_bad(source[13]):
            q += self.get_path_spec(source[13])
          
        # add description
        if not helpers.is_bad(source[14]):
            q += """;
                wnp:description \'""" + helpers.clean_string(source[14]) + "\'"
        
        q += """.}"""  
                
        return q 