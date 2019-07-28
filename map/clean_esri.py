#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 20:55:39 2019

@author: lavanyasingh
"""

import csv
import os
os.chdir("/Users/lavanyasingh/Desktop/GSC2O19internet_archive/")
#import geojson 
import geopy
import us
import pycountry
from countryinfo import CountryInfo
import helpers


gn = geopy.geocoders.GeoNames(username = "lavanya_archive")
geopy.geocoders.options.default_timeout = None

def read_in():
    sources = []
    total = 0
    with open("data/raw/all_raw_cleaned3.csv", 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for line in reader:
            total += 1
            sources.append(["".join(element).strip().lower().replace(" ", "") for element in line])
    print("DONE READING")
    return sources

def get_country_iso(country):
    c = pycountry.countries.search_fuzzy(country)[0]
    return c.alpha_2

def get_country_coord(country):
    country_off = pycountry.countries.search_fuzzy(country)[0].official_name
    c = CountryInfo(country_off)
    try:
        capital = c.capital()
    except KeyError:
        capital = CountryInfo(country).capital()
    return (get_country_city_coord(country, capital))
    
def get_city_coord(city):
    code = (gn.geocode(city, exactly_one=True))
    return code.latitude, code.longitude
    
def get_state_coord_us(state):
    st = us.states.lookup(state)
    capital =  st.capital
    return get_city_coord(capital, "United State of America")

def get_country_city_coord(country, city):
    try:
        code = (gn.geocode(city, exactly_one=True, country = get_country_iso(country)))
        return code.latitude, code.longitude
    except (geopy.exc.GeocoderTimedOut, KeyError) as e:
        print(e)
        return ""

def get_coords(sources):
    data = {}
    coord = ""
    for source in sources:
        if not helpers.is_bad(source[9]):
            if not helpers.is_bad(source[0]):
                coord = get_country_city_coord(source[0], source[9])
            else:
                coord = get_city_coord(source[9])
        elif (not helpers.is_bad(source[8]) and source[0]
        in ["united states", "unitedstatesofamerica", "us", "usa"]):
                coord = get_state_coord_us(source[9])
        elif not helpers.is_bad(source[0]):
            coord = get_country_coord(source[0])
        if coord != "": 
            data.update({source[1]: coord})
    return data

coords = get_coords(read_in())
            
