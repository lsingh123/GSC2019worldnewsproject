#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 12:45:23 2019

@author: lavanyasingh
"""

import csv

def clean():
    with open("data/codes2.csv", 'r') as f:
        reader = csv.reader(f, delimiter=',')