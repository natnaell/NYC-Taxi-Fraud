#This program performs a parameter sweep for the different clustering algorithms. Prints the sum of the weighted sum of squares of all clusters.
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


def data_prep():
	df = pd.read_csv('clean_taxi_8.csv')
	df = df[::3]
	df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])
	df['hour'] = df['pickup_datetime'].dt.hour
	df['morning'] = (df['hour'] >=5) & (df['hour'] <11)
	df['afternoon'] = (df['hour'] >=11) & (df['hour'] <4)
	df['rush'] = (df['hour'] >=4) & (df['hour'] <8)
	df['evening'] = df['hour'] >=8
	df['dow'] = df['pickup_datetime'].dt.dayofweek
	df['weekend'] = df['dow'] >=4


	df['scaled_pickup_latitude'] = pow(8,.5)*scale(df['pickup_latitude'])
	df['scaled_pickup_longitude'] = pow(8,.5)*scale(df['pickup_longitude'])
	df['scaled_dropoff_latitude'] = pow(8,.5)*scale(df['dropoff_latitude'])
	df['scaled_dropoff_longitude'] = pow(8,.5)*scale(df['dropoff_longitude'])
	df['scaled_passenger_count'] = scale(df['passenger_count'].astype(float))
	df['scaled_weekend'] = scale(df['weekend'].astype(float))
	df['scaled_morning'] = scale(df['morning'].astype(float))
	df['scaled_afternoon'] = scale(df['morning'].astype(float))
	df['scaled_rush'] = scale(df['rush'].astype(float))
	df['scaled_evening'] = scale(df['evening'].astype(float))
	return df


def sweep(df,model):
	if model=='kmeans':
		for i in [100,200,500,1000,2000,2500]:
			ms = MiniBatchKMeans(n_clusters=i)
			fit_and_evaluate(df,ms,model,i)
	elif model=='dbscan':
		for i in [50,100,200,500,1000]:
			ms = DBSCAN(min_samples = i)
			fit_and_evaluate(df,ms,model,i)
	elif model=='meanshift':
		for i in [.01,.02,.03,.04]:
			ms = MeanShift(bandwidth=i, bin_seeding=True)
			fit_and_evaluate(df,ms,model,i)


def fit_and_evaluate(df,ms,model,i):
	cols = ['scaled_weekend','scaled_passenger_count','scaled_pickup_latitude','scaled_pickup_longitude','scaled_dropoff_latitude','scaled_dropoff_longitude','scaled_morning','scaled_afternoon','scaled_rush','scaled_evening']
	ms_model = ms.fit(df[cols])
	df['cluster']=ms_model.labels_
	if model=='dbscan':
		df = df[df['cluster']!=-1]
	#df.groupby(['cluster'])['pickup_latitude','pickup_longitude','dropoff_latitude','dropoff_longitude'].std()

	counts = pd.DataFrame(df['cluster'].value_counts(),columns=['count'])
	wgss = pow(pow(df.groupby(['cluster'])[cols].std(),2).sum(axis=1),.5)
	cluster_wgss = pd.DataFrame(wgss,columns=['wgss'])
	counts = counts.merge(cluster_wgss,left_index=True,right_index=True)
	counts['weighted_wgss'] = counts['count'] * counts['wgss']
	print model,i
	print counts['weighted_wgss'].mean()


if __name__ == "__main__":
	model = sys.argv[1]
	df = data_prep()
	sweep(df,model)
