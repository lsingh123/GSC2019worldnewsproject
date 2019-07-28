#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 15:42:20 2019

@author: lavanyasingh
"""

import csv
import os
os.chdir(os.path.dirname(os.getcwd()))
import geopy
import pycountry
import os, sys
sys.path.append(os.getcwd())
import helpers
from countryinfo import CountryInfo

class mapDataMaker():
    
    PATH = os.getcwd() + "/data/"
    
    def __init__(self, infile, outfile):
        self.gn = geopy.geocoders.Nominatim(user_agent = "lavanya_archive")
        geopy.geocoders.options.default_timeout = None
        self.infile = infile
        self.outfile = outfile
    
    def get_country_coord(self, country):
        country = country.strip().lower()
        try:
            country_off = pycountry.countries.search_fuzzy(country)[0].official_name
        except AttributeError:
            country_off = pycountry.countries.search_fuzzy(country)[0].name
        c = CountryInfo(country_off)
        try:
            capital = c.capital()
        except KeyError:
            try:
                capital = CountryInfo(country).capital()
            except KeyError:
                return ""
        return (self.get_country_city_coord(country, capital))
    
    def get_country_city_coord(self, country, city):
        try:
            code = (self.gn.geocode({"city":city, "country":country, 
                                "countrycodes":self.get_country_iso(country)}))
            return code.latitude, code.longitude
        except (geopy.exc.GeocoderTimedOut, KeyError) as e:
            print(e)
            return ""
        
    def get_country_iso(self, country):
        c = pycountry.countries.search_fuzzy(country)[0]
        return c.alpha_2
    
    def get_sources(self):
        total = 0
        with open(self.PATH + "raw/" + self.infile, 'r') as inf:
            reader = csv.reader(inf, delimiter=',')
            with open(self.PATH + self.outfile, 'w') as outf:
                w = csv.writer(outf, delimiter= ',', quotechar = '"', 
                               quoting = csv.QUOTE_MINIMAL)
                for line in reader:
                    total += 1
                    if total % 500 == 0:
                        if not helpers.is_bad(line[0]):
                            coord = self.get_country_coord(line[0])
                        if coord != "": 
                            w.writerow([coord[0], coord[1], line[1]])
        print("WROTE GEODATA")

if __name__ == "__main__":
    mapmaker = mapDataMaker("all_raw_cleaned.csv", "geodata.csv")
    mapmaker.get_sources()
        
