# worldnews

Code developed for the World News Project during Google Summer of Code 2019.
*Note: This repository contains operationalized code to be used as a long term
resource. For old/exploratory scripts, please see: https://github.com/lsingh123/internet_archive_old*

## Conventions

- deduplication occurred on the top-level private domain as produced by `helpers.truncate(url)`
- data is stored in a CSV with the following columns: `['country', 'url', 'title', 'language', 'type', 'title native language', 'paywall', 'metasource', 'state', 'town', 'wikipedia name', 'redirects?', 'wikipedia link']` 
- the jena fuseki triple store has one graph for each news source

## Helpers

`helpers.py` contains helper functions and conventions for storing data in
CSV's. `googlesheethelpers.py` contains helper functions for accessing Google
Sheets. This file *is not used anymore*, but was useful at the beginning of the
project when data was stored in a Google Sheet.

## Collection

Scripts that start with `collect` such as `collect_mediacloud.py` are used to
scrape news sources from a particular metasource. The naming convention for such
scripts is `collect_[metasource].py`

## Cleaning

Scripts starting with `clean` are used for processing, deduplicating,
truncating, and cleaning the data.

## Tableau

`tableau_prep.py` is used to create a CSV of URLs, coordinates, and countries
to be used to create visulizations in Tableau. `tableau_scrape.py` was used to
scrape a list of countries and coordinates from Google Public Data. This list
was used in `tableau_prep.py`.

## Fuseki

Scripts starting with `fuseki` are used to prepare and load data into an Apache
Jena triplestore. `fuseki_feed.py` is the only script that you'll need to run.
`fuseki_graph_spec.py` contains a helper class used to build the graph spec.

`fuseki_feed.py -h` will output instructions for running the script from the
command line.

```
$ python fuseki_feed.py -h
usage: fuseki_feed.py [-h] [-inf [INFILE]] [-url URL]
                      [-g [{overwrite,no_overwrite,first_load}]]

Feed data into fuseki database

optional arguments:
  -h, --help            show this help message and exit
  -inf [INFILE], --infile [INFILE]
                        csv file to read URLs in from

required named arguments:
  -url URL              database endpoint
  -g [{overwrite,no_overwrite,first_load}], --graph_spec [{overwrite,no_overwrite,first_load}]
                        graph spec function to use. see fuseki_graph_spec.py
                        for the different functions. "overwrite" overwrites
                        existing metadata. "no_overwrite" respects existing
                        metadata. "first_load" assumes an empty datastore.
```

For more information on querying and updating the database, please
see: https://docs.google.com/document/d/1rY32moyAVndtINysWYF5c5rhRtSX6OyTH5rkGc6vzoQ

## Metadata

Scripts starting with `meta` are used for metadata collection and processing
after the fact. `meta_scrape.py` uses Kenji's cluster of headless browsers to
scrape and parse the HTML for each news source to identify metadata.

## Visualizations

Scripts in `/visualizations` use matplotlib to make visualizations of the data.
`make_venn.py` makes venn diagrams of the overlapping URLs from certain different
metasources. `viz_metasources.py` creates a bar chart of the number of URLs from
each metasource. 

## Contact

`lsingh@college.harvard.edu`
