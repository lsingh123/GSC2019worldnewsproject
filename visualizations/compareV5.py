#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 13:03:31 2019

@author: lavanyasingh
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 15:09:18 2019

@author: lavanyasingh
"""

#investigating why there's such little overlap between datastreamer and media cloud's sources

import os
import csv
from matplotlib_venn import venn2, venn2_circles, venn3, venn3_circles
import helpers

os.getcwd()
os.chdir('/Users/lavanyasingh/Desktop/GSC2O19internet_archive')

#BE VERY CAREFULY WHEN EDITING THIS SHEET
#ONLY EDIT HERE AFTER THOROUGH TESTING
real_deal = '131Y_PxkJgibJ117fsQrfc79lVi6MLGWfCBBJvrdQuN8'
#USE THIS SHEET TO TEST 
test = '12yV42AFnUecXFXwaLUpz6Hqh9VpRp6gtap8x6xEAp7U'

spreadsheet_id = real_deal

service = helpers.initialize()

#returns a list of source URLS from a google sheet
def get_sources_sheet():
    raw, total = helpers.get_sources(spreadsheet_id, service)
    sources = []
    for item in raw:
        for url in item:
            sources.append(helpers.truncate(item[url][2]))
    return sources
        

def compare_2():
    og_list = set(get_sources_sheet())
    wn_list = set(helpers.read_csv_list('data/wn_sources.csv'))
    print(og_list[0])
    print(wn_list[0])
    venn2([og_list, wn_list], ('Existing', 'WikiNews'))
    plt.savefig('visualizations/existing vs wikinews.png')
    
compare_2()