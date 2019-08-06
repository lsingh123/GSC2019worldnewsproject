# worldnews

Code developed for the World News Project during Google Summer of Code 2019.

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

For more information on querying and updating the database, please
see: https://docs.google.com/document/d/1rY32moyAVndtINysWYF5c5rhRtSX6OyTH5rkGc6vzoQ

## Metadata

Scripts starting with `meta` are used for metadata collection and processing
after the fact. 
