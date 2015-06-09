rounder.py

Description:
It takes every trip_data month in the dataset and it rounds the GPS coordinates
to the 3rd decimal.

Output:
A new file with the rounded data for every month.
trip_data_n_r3.csv

combine.py

Description:
It combines every month's trip and fare data into one file.

Output:
A new file with the combined data for every month.
taxi_n.csv

cleaner.py

Description:
It takes every month in the dataset and it cleans it up, removing duplicates,
removing hack licences that have and MD5 encoded '0' value, removing short trips,
Lat/Long = '0', removing trips from or to outside Manhattan.

Output:
A new file with the clean data for every month.
clean_taxi_n.csv

superv_learning3.py

Description:
It runs the different models.
Current version only runs boosting, since it had the highest accuracy and does not
do parameter sweeping, since we already know the best parameters. But all that
can be uncommented.
It reads September and October, does feature engeenier (the same that unsupevised)
and then trains on September and predict on October.
Takes the difference of the prediction and the real fare, scales it, normalizes it,
and aggregates it by driver.


Output:
One file with the aggregated score by driver
ride_score_clean_boosting_final.csv
One file with the core for each ride
driver_score_clean_boosting_final.csv



weighting_analysis.py

Description:
This file evaluates the effect of different weights on the latitude and longitude
coordinates for pickup and dropoff. It defaults to using kmeans.

Output:
Prints out the mean sum of variances for the latitude and longitude coordinates for
all clusters.


unsupervised_learning.py

Description:
This file runs the unsupervised pipeline using three different clustering
algorithms (kmeans, mean shift, dbscan). All three models take in the same
features. Each trips is assigned a score based off its position within the cluster
as well as the cluster's within group sum of squsres. The scores are then
aggregated by driver and normalized.

Output:
Three csv outputs that have each hack license and the associated score.
kmeans_driver_scores.csv
meanshift_driver_scores.csv
dbscan_driver_scores.csv


parameter_sweep.py

Description:
Runs through different parameters for each clustering algorithm. Evaluates based on
the total within group sum of squares.
Minibatch k-means: number of clusters
Mean Shift:        bandwidth size
DBSCAN:            neighborhood size

Output:
Prints out the total within group sum of squares for each iteration.


**********************
****** database/ ******
**********************

taxi_compile.sh

Description:
"Combine separate month data files into a single CSV for copying to the PostgreSQL database"

Output:
"taxi_combined.csv"


upload.sql

Description:
"Copies the CSV files with entire year of data to the PostgreSQL database"

Output:
""


create_indexes.sql

Description:
"Add columns for the month, day of week, hour of day and and create indexes on these, as well as on the hack license."

Output:
""


**********************
** descriptive_stats/ **
**********************

summarize*.sh

Description:
"Queries the database for descriptive statistics, in particular the mean and standard deviation of fare_amount, trip_distance, and trip_time_in_secs. Reports summary stats for the entire year, for each month, for random days, and for hour of the day"

Output:
"*_summary.txt"

**********************
****** analysis/ ******
**********************

create_plots.sh

Description:
"Contains commands to download a week of data and generate plots for use in the presentation and report."

Output:
"Data downloaded from the database and figures showing fare/distance/time distributions."

explore.py

Description:
"Functions to produce nice-ish plots showing the distributions of fares, distances, and times for different days of the week and hours of the day."

Output:
"matplotlib figures and axes."

dl_range.sh

Description:
"Given a date range, copies all records from the database with pickup date within that range (in this case 10-7-2013 to 10-14-2013) to a CSV file. "

Output:
"combined_2013-10-7_2013-10-14.csv"

load_and_plot.py

Description:
"Load the data downloaded using 'dl_range.sh', import the plotting functions contained in 'explore.py', and create plots showing the distribution of fares, distances, and times for different days of the week and hours of the day."

Output:
"All of the files in the 'figures/' directory."

test_plots_and_clustering.ipynb

Description:
"Test out the plotting functions contained in 'explore.py', and also take a first crack at using various clustering algorithms."

Output:
"none"

driver_compare.ipynb

Description:
"Take driver scores calculated using the various unsupervised/supervised analysis and compare the ranking of drivers by each method. Also generate some plots showing the results of the comparison."

Output:
"'Rate of Agreement' plots."
