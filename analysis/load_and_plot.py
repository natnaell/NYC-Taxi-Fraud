#!/usr/bin/python

import pandas as pd
import numpy as np
import sys

df = pd.read_csv(sys.argv[1], index_col=0)

import explore

cols = ['fare_amount','trip_distance','trip_time_in_secs']

for d in range(1,8):
    ss = df.ix[df.day_of_week==d,:]
    for c in cols:
        explore.plot_hours(ss, c, figdir='day'+str(d))
        explore.plot_days(ss, c)
        explore.plot_days_same(ss, c)
