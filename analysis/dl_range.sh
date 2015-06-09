#!/bin/bash

# Pull data in a date range from the AWS database
# Accepts 4 arguments: from month, from day, to month, to (but not including) day

# EXAMPLE:
# sh dl_range.sh 1 5 2 6

# will download all data for which the pickup date is on or after 1/5/2013 and 
# UP TO BUT NOT INCLUDING 2/6/2013 (so you get all pickups up to midnight on 2/5/2013
# Trip and fare data are downloaded to separate files

from_date="2013-$1-$2"
to_date="2013-$3-$4"

table="combined"
datafile="${table}_${from_date}_${to_date}.csv"

psql -h dssgsummer2014postgres.c5faqozfo86k.us-west-2.rds.amazonaws.com -p 5432 -U harris classes -c "\copy (SELECT * FROM taxi.${table} WHERE date(pickupdatetime)>=date('$from_date') AND date(pickupdatetime)<date('$to_date')) to '$datafile' csv header"
