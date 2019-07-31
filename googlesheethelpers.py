#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 13:58:37 2019

@author: lavanyasingh
"""
# helper functions specifically for automated access to google sheets
# was useful at start of project when data was stored in a google sheet

import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def initialize():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
       with open('token.pickle', 'rb') as token:
           creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
            
    service = build('sheets', 'v4', credentials=creds)
    return service

#returns list of row dictionaries in url:row format (cleans URLS)
#each row is a string list with one element per cell
#also returns total number of rows
def get_sources(spreadsheet_id, service):
    result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range='A:H').execute()
    count = 1
    sources = []
    numRows = result.get('values') if result.get('values')is not None else 0
    for row in numRows:
        count += 1
        try:
            url = truncate(row[2])
            new_row = []
            for i in range(9):
                try: new_row.append(url) if i == 2 else new_row.append(row[i])
                except IndexError: new_row.append("") 
            sources.append({url:new_row})
        except IndexError as e:
            print(count, e)
    return sources, count