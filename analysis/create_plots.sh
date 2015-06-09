#!/bin/bash

bash dl_range.sh 10 7 10 14

datafile="combined_2013-10-7_2013-10-14.csv"

python load_and_plot.py $datafile
