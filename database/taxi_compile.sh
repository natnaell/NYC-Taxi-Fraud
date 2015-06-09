#!/bin/bash

# This script combines multiple csv files where the first row contains column names into a single csv file called "taxi_compiled.csv" where the first row contains column names.
# It is used to compile the csv files with data from separate months into a single file to be copied to the PostgreSQL database.

for m in $(seq 1 12); do
  filename="/local/taxi/Santiago/clean_taxi_$m.csv"
  if [ $m -eq 1 ]
  then
    cp $filename taxi_compiled.csv
  else
    sed '1d' $filename >> taxi_compiled.csv
  fi
done
