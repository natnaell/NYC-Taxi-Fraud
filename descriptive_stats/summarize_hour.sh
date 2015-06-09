#!/bin/bash

stats="avg stddev_samp"
cols="fare_amount trip_time_in_secs trip_distance"

sel="avg(fare_amount), avg(trip_time_in_secs), avg(trip_distance), stddev_samp(fare_amount), stddev_samp(trip_time_in_secs), stddev_samp(trip_distance)"

for i in $(seq 0 23); do
 echo
 echo "Hour of day: $i"
 echo
 echo "SELECT $sel FROM taxi.combined WHERE hour_of_day=$i" > temp.sql
 psql -h dssgsummer2014postgres.c5faqozfo86k.us-west-2.rds.amazonaws.com -p 5432 -U harris -d classes -f temp.sql 
done

rm temp.sql
