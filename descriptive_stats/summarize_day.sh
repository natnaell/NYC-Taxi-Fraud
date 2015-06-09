#!/bin/bash

stats="avg stddev_samp"
cols="fare_amount trip_time_in_secs trip_distance"

sel="avg(fare_amount), avg(trip_time_in_secs), avg(trip_distance), stddev_samp(fare_amount), stddev_samp(trip_time_in_secs), stddev_samp(trip_distance)"

for i in $(seq 1 30); do
 m=$(( RANDOM % 12 + 1 ))
 d=$(( RANDOM % 28 + 1 ))
 from_date="2013-$m-$d"

 echo
 echo "Date: $from_date"
 echo
 echo "SELECT $sel FROM taxi.combined WHERE date(pickupdatetime)=date('$from_date')" > temp.sql
 psql -h dssgsummer2014postgres.c5faqozfo86k.us-west-2.rds.amazonaws.com -p 5432 -U harris -d classes -f temp.sql 

done

for i in $(seq 1 7); do
 echo
 echo "Day of Week: $i"
 echo
 echo "SELECT $sel FROM taxi.combined WHERE day_of_week=$i" > temp.sql
 psql -h dssgsummer2014postgres.c5faqozfo86k.us-west-2.rds.amazonaws.com -p 5432 -U harris -d classes -f temp.sql 
done

rm temp.sql
