#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 10:00:17 2019

@author: lavanyasingh
"""

import mediacloud.api
import csv

class mcGrabber():
    
    # this is my Media Cloud API key
    KEY = '6e5564bc0c07edb1c307a8a7a34adbcb19a6d27c3d202987a1426a9066341308'
    COUNTRY_ID = 1935
    
    def __init__(self, path="data/"):
        self.mc = mediacloud.api.MediaCloud(self.KEY)
        self.path = path
    
    # get a list of tags within a tag_set_id
    # returns dict in Country:tag_id format
    # in practice I use this to get all the tags within the tag_sets_id 
    # corresponding to country (so all the tags for each country)
    def get_by_id(self, id):
        last_proc_tag = 0
        items = {}
        fetched = self.mc.tagList(tag_sets_id = self.COUNTRY_ID, 
                                      last_tags_id = last_proc_tag, rows = 100)
        # keep fetching until we hit the bottom of the barrel
        while len(fetched) >= 95: 
            for tag in fetched:
                items[tag['label']] = tag['tags_id']
            fetched = self.mc.tagList(tag_sets_id = self.COUNTRY_ID, 
                                      last_tags_id = last_proc_tag, rows = 100)
            last_proc_tag = fetched[-1]['tags_id']
        
        # add the last few results to items
        for tag in fetched:
                items[tag['label']] = tag['tags_id']
        return items
    
    #get list of all media sources and write to a csv
    #columns: country, url, title, language, type
    def get_media(self):
        
        # get the country tags
        countries = self.get_by_id(self.COUNTRY_ID)
        
        with open(self.path + 'mc_sources_meta.csv', mode = 'w') as f:
            w = csv.writer(f, delimiter=',', quotechar='"', 
                           quoting=csv.QUOTE_MINIMAL)
            w.writerow(['country', 'source url', 'title', 'language', 'type'])
            for country in countries:
                last_proc_id = 0
                fetched = self.mc.mediaList(tags_id = countries[country], 
                                                rows = 100, last_media_id = 
                                                last_proc_id)
                
                # keep fetching until we hit the bottom of the barrel
                while len(fetched) >= 95:
                    
                    for item in fetched:
                        #each item will definitely have a title and url
                        title = item['name']
                        url = item['url']
                        #items may or may not have languages and types
                        #so we check for Nonetypes to avoid a type error
                        lang, t = None, None
                        if item['metadata']['language'] != None: 
                            lang = item['metadata']['language']['label']
                        if item['metadata']['media_type'] != None: 
                            t = item['metadata']['media_type']['label']
                        w.writerow([country, url, title, lang, t])
                        
                    last_proc_id = fetched[-1]['media_id']
                    fetched = self.mc.mediaList(tags_id = countries[country], 
                                                rows = 100, last_media_id = 
                                                last_proc_id)
                # write the last few
                for item in fetched:
                        #each item will definitely have a title and url
                        title = item['name']
                        url = item['url']
                        #items may or may not have languages and types
                        #so we check for Nonetypes to avoid a type error
                        lang, t = None, None
                        if item['metadata']['language'] != None: 
                            lang = item['metadata']['language']['label']
                        if item['metadata']['media_type'] != None: 
                            t = item['metadata']['media_type']['label']
                        w.writerow([country, url, title, lang, t])
                       
if __name__ == '__main__':
    mc = mcGrabber()
    mc.get_media()

        
    
        
