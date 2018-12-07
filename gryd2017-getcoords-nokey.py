#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 09:05:48 2018

@author: Ben Shulman
"""

import sys
import numpy
import pandas
from itertools import islice
import requests

# data in
gryddata = pandas.read_csv('/Users/Ben/Dropbox/PhD/Research/gryd/RAW_IR__Master_List_10.1.2018.csv')

# filter gryd to 2017
gryddata.iloc[:, 10] = pandas.to_datetime(gryddata.iloc[:, 10])
gryd2017 = gryddata[(gryddata.iloc[:, 10] > '2016-12-31 00:00:00') &
                    (gryddata.iloc[:, 10] < '2018-1-1 00:00:00')]

# query coordinates from google
def getcoord(address):
    addresst = address + ' Los Angeles CA'
    addresst = addresst.replace('&', 'at').replace(' and ', ' at ').replace('#', '%23').replace(' ', '+')
    # will need to add an API key here to use this
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + addresst + '&key='
    response = requests.get(url)
    resp_json_payload = response.json()
    coord = resp_json_payload['results'][0]['geometry']['location']
    return coord

for index, row in islice(gryd2017.iterrows(), 0, None):
    address = row['Address of Incident or Intersection 1_53']
    thecoord = getcoord(address)
    gryd2017.loc[index, 'lat'] = tuple(thecoord.values())[0]
    gryd2017.loc[index, 'lng'] = tuple(thecoord.values())[1]

gryd2017.to_csv('/Users/Ben/Dropbox/PhD/Research/gryd/gryd2017-coords.csv')
