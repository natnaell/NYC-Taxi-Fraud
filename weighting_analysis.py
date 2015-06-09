#This program iterates through different weights for the latitude and longitude coordinates in order to make sure each each cluster is geographically similar within.
import pandas as pd
from datetime import datetime
from sklearn.preprocessing import scale
from sklearn.cluster import MeanShift, estimate_bandwidth,KMeans,MiniBatchKMeans,DBSCAN
import csv
import sys
import numpy as np
from scipy.stats import logistic
from scipy.stats import norm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

model = sys.argv[1]

df = pd.read_csv('clean_taxi_8.csv')
df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])
df['hour'] = df['pickup_datetime'].dt.hour
df['morning'] = (df['hour'] >=5) & (df['hour'] <11)
df['afternoon'] = (df['hour'] >=11) & (df['hour'] <4)
df['rush'] = (df['hour'] >=4) & (df['hour'] <8)
df['evening'] = df['hour'] >=8
df['dow'] = df['pickup_datetime'].dt.dayofweek
df['weekend'] = df['dow'] >=4


for i in range(1,11):
	df['scaled_pickup_latitude'] = pow(i,.5)*scale(df['pickup_latitude'])
	df['scaled_pickup_longitude'] = pow(i,.5)*scale(df['pickup_longitude'])
	df['scaled_dropoff_latitude'] = pow(i,.5)*scale(df['dropoff_latitude'])
	df['scaled_dropoff_longitude'] = pow(i,.5)*scale(df['dropoff_longitude'])
	df['scaled_passenger_count'] = scale(df['passenger_count'].astype(float))
	df['scaled_weekend'] = scale(df['weekend'].astype(float))
	df['scaled_morning'] = scale(df['morning'].astype(float))
	df['scaled_afternoon'] = scale(df['morning'].astype(float))
	df['scaled_rush'] = scale(df['rush'].astype(float))
	df['scaled_evening'] = scale(df['evening'].astype(float))

	cols = ['scaled_weekend','scaled_passenger_count','scaled_pickup_latitude','scaled_pickup_longitude','scaled_dropoff_latitude','scaled_dropoff_longitude','scaled_morning','scaled_afternoon','scaled_rush','scaled_evening']

	if model=='kmeans':
		ms = MiniBatchKMeans(n_clusters=2000)
	elif model=='dbscan':
		ms = DBSCAN(min_samples = 100)
	elif model=='meanshift':
		ms = MeanShift(bandwidth=0.01, bin_seeding=True)


	ms_model = ms.fit(df[cols])
	df['cluster']=ms_model.labels_
	if model=='dbscan':
		df = df[df['cluster']!=-1]
	counts = pd.DataFrame(df['cluster'].value_counts(),columns=['count'])
	latlon_std = pd.DataFrame( df.groupby(['cluster'])['pickup_latitude','pickup_longitude','dropoff_latitude','dropoff_longitude'].std().mean(axis=1) ,columns=['std'])
	counts = counts.merge(latlon_std,left_index=True,right_index=True)
	counts['weighted_std'] = counts['count'] * counts['std']
	print i
	print counts['weighted_std'].mean()
