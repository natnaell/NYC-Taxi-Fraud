#!/bin/bash

stats="avg stddev_samp"
cols="fare_amount trip_time_in_secs trip_distance"

for s in $stats; do
 for c in $cols; do
  echo "$s($c)"
  echo
  echo "SELECT $s($c) FROM taxi.combined" > temp.sql
  psql -h dssgsummer2014postgres.c5faqozfo86k.us-west-2.rds.amazonaws.com -p 5432 -U harris -d classes -f temp.sql 
 done
done

rm temp.sql
