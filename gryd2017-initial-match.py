#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 13:59:25 2018

@author: Ben Shulman
"""

import sys
import geopy.distance
import numpy
import pandas

# data in
lapddata = pandas.read_csv('/Users/Ben/Dropbox/PhD/Research/gryd/CRIME-2017-CityWide-AGG-HOM-ROBB-to-6-9-18.csv')
gryddata = pandas.read_csv('/Users/Ben/Dropbox/PhD/Research/gryd/gryd2017-coords.csv')

# prepare dates
lapddata.loc[:, 'BEGDATE'] = pandas.to_datetime(lapddata.loc[:, 'BEGDATE'])
gryddata.loc[:, 'Date of incident_49'] = pandas.to_datetime(gryddata.loc[:, 'Date of incident_49'])

# drop some of the 2018 lapd data
# we're only matching 2017 events
# this saves a bunch of comparisons
lapddata = lapddata[lapddata.loc[:, 'BEGDATE'] < '2018-1-10 00:00:00']

# match search
gryddata['disttime'] = numpy.NaN
gryddata['distspace'] = numpy.NaN
gryddata['distcomb'] = numpy.NaN
gryddata['nextdist'] = numpy.NaN
gryddata['inimatch'] = numpy.NaN
lapdmatches = pandas.DataFrame(index = numpy.arange(len(gryddata)),
                               columns = lapddata.columns)
for i in range(len(gryddata)):
    
    # compare time
    disttime = numpy.array(len(lapddata) * [numpy.NaN])
    for j in range(len(lapddata)):
        disttime[j] = (lapddata.loc[j, 'BEGDATE']
                        - gryddata.loc[i, 'Date of incident_49']).days
    
    # compare space
    distspace = numpy.array(len(lapddata) * [numpy.NaN])
    for j in range(len(lapddata)):
        if disttime[j] == 0: # only compare events that happened on the same day
            distspace[j] = geopy.distance.distance(
                    (lapddata.loc[j, 'lat'], lapddata.loc[j, 'lng']),
                     (gryddata.loc[i, 'lat'], gryddata.loc[i, 'lng'])).m
                    
    # combine the two distances
    distcomb = (abs(disttime) + 1) * distspace
    
    # write them to df
    gryddata.loc[i, 'distcomb'] = numpy.nanmin(distcomb)
    gryddata.loc[i, 'disttime'] = disttime[numpy.nanargmin(distcomb)]
    gryddata.loc[i, 'distspace'] = distspace[numpy.nanargmin(distcomb)]
    
    # note the distance of the next best match
    gryddata.loc[i, 'nextdist'] = sorted(distcomb[~numpy.isnan(distcomb)])[1]
    
    # was the match close enough?
    gryddata.loc[i, 'inimatch'] = 1 if (gryddata.loc[i, 'distcomb'] < 500) & \
                                        (gryddata.loc[i, 'nextdist'] > 500) \
                                        else 0
                                        
    # store the matched lapd row
    lapdmatches.loc[i, :] = lapddata.loc[numpy.nanargmin(distcomb), :]
    
    # print counter
    print(i)

matchesout = pandas.concat([gryddata, lapdmatches], axis = 1)
matchesout.to_csv('/Users/Ben/Dropbox/PhD/Research/gryd/gryd2017-inimatch.csv')
