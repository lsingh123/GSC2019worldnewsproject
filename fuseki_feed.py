#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 11:28:34 2019

@author: lavanyasingh
"""

from prefixes import prefixes
import helpers
import csv
from fuseki_graph_spec import graphGenerator
import argparse
        

class Feeder:

    # graph spec_maker should be a function that returns a graph spec
    # from the graphGenerator class defined in graph_spec.py
    def __init__(self, graph_spec_maker, infile, url):
        self.get_graph_spec = graph_spec_maker
        self.infile = infile
        self.endpoint = url
        self.write_metasources()

    def write_metasources(self):
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
            wni:prensaescrita wdt:P1448 "Prensa Escrita".
            wni:commoncrawl wdt:P1448 "Common Crawl".
            wni:lion wdt:P1448 "LION Publishers".}
        } """
        helpers.send_query(self.endpoint, query)
        print('successfully wrote meta sources')

    #takes in a list of CSV rows
    def dump_all(self, sources):
        counter = 0
        q = ''
        for source in sources:
            s = self.get_graph_spec(source)
            counter += 1
            q  += s
            if counter % 1000 == 0:
                print("DUMPED {counter} SOURCES".format(counter=counter))
                query = prefixes + """
                INSERT DATA {
                """ + q + """} """
                q = ''
                # break for bad queries
                try:
                    helpers.send_query(self.endpoint, query)
                except:
                    with open('data/logfile', 'w') as f:
                        f.write(query)
                        print("BAD QUERY")
                    break
        print("DONE")

    def read_in(self):
        sources = []
        with open(self.infile, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            for line in reader:
                line[7] = line[7].strip(" ").split(" ")
                line[13] = line[13].strip(" ").split(" ")
                sources.append(line)
                print("READING SOURCE {sources}".format(sources=len(sources)), end="\r")
        print("\nDONE READING")
        return sources

# create argument parser
def create_parser():
    argp = argparse.ArgumentParser(
            description='Feed data into fuseki database')
    argp.add_argument('-inf', '--infile', nargs='?',
                      default='data/all_metadata.csv', type=str,
                      help='csv file to read URLs in from')
    requiredNamed = argp.add_argument_group('required named arguments')
    requiredNamed.add_argument('-url', default='http://wwwb-db01.us.archive.org:3030/wn/update', type=str,
                      help='database endpoint')
    requiredNamed.add_argument('-g', '--graph_spec', nargs='?', 
                      choices = ['overwrite', 'no_overwrite', 'first_load'],
                      default='no_overwrite', type=str,
                      help='''graph spec function to use. see fuseki_graph_spec.py for the different functions. 
                      "overwrite" overwrites existing metadata. 
                      "no_overwrite" respects existing metadata.
                      "first_load" assumes an empty datastore.''')
    return argp


if __name__ == '__main__':
    argp = create_parser()
    args = argp.parse_args()
    generator = graphGenerator()
    graph = args.graph_spec
    if graph == 'no_overwrite':
        graph_spec = generator.no_overwrite
    elif graph == 'overwrite':
        graph_spec = generator.overwrite
    elif graph == 'first_load':
        graph_spec = generator.first_load
    feeder = Feeder(graph_spec_maker=graph_spec, infile=args.infile, url=args.url)
    sources = feeder.read_in()
    feeder.dump_all(sources)