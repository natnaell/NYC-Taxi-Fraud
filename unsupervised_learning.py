#This program uses unsupervised machine learning to assign taxi drovers a fraudulent score.
import pandas as pd
import sys
from datetime import datetime
from sklearn.preprocessing import scale
from sklearn.cluster import MeanShift, estimate_bandwidth,KMeans,MiniBatchKMeans,DBSCAN
import csv
import numpy as np
from scipy.stats import logistic
from scipy.stats import norm
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt



def read_data():
	df = pd.read_csv('clean_taxi_10.csv')
	#df = df[::10]
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


def fit_model(df,model,cols):
	if model=='kmeans':
	        ms = MiniBatchKMeans(n_clusters=2000)
	elif model=='dbscan':
	        ms = DBSCAN(min_samples = 500)
	elif model=='meanshift':
	        ms = MeanShift(bandwidth=.1, bin_seeding=True)
	ms_model = ms.fit(df[cols])
	df['cluster']=ms_model.labels_
	if model=='dbscan':
	        df = df[df['cluster']!=-1]
	return df
#df.groupby(['cluster'])['pickup_latitude','pickup_longitude','dropoff_latitude','dropoff_longitude'].std()

def create_scores(df,model,cols):	
	df = fit_model(df,model,cols)
	wgss = pow(pow(df.groupby(['cluster'])[cols].std(),2).sum(axis=1),.5)
	cluster_wgss = pd.DataFrame(wgss,columns=['wgss'])
	cluster_wgss['cluster'] = np.unique(df['cluster'])
	cluster_wgss['cluster_mean'] = df.groupby(['cluster'])['fare_amount'].mean()
	cluster_wgss['cluster_std'] = df.groupby(['cluster'])['fare_amount'].std()
	#import pdb
	#pdb.set_trace()
	cluster_wgss = cluster_wgss[ cluster_wgss.notnull().all(1) ]
	df = df.merge(cluster_wgss,on='cluster')
	df = df[ df['cluster_std']!=0 ]
	df.loc[ df['wgss'] ==0,'wgss'] = .001
	df['score'] = ( df['fare_amount'] - df['cluster_mean'] ) / df['cluster_std']
	df['weighted_score']=df['score']/df['wgss']
	driver_scores=pd.DataFrame( df.groupby(['hack_license'])['weighted_score'].sum() , copy = True).sort(columns=['weighted_score'])
	driver_scores = driver_scores[ driver_scores.notnull().all(1) ]
	driver_scores['normal_prob'] = np.apply_along_axis( norm.cdf, 0, scale( driver_scores['weighted_score'] ) )
	driver_scores.index.names=['hack_license']
	driver_scores[ 'normal_prob' ].to_csv(model+'_driver_scores.csv')


if __name__ == "__main__":
	model = sys.argv[1]
	df = read_data()
	cols = ['scaled_weekend','scaled_passenger_count','scaled_pickup_latitude','scaled_pickup_longitude','scaled_dropoff_latitude','scaled_dropoff_longitude','scaled_morning','scaled_afternoon','scaled_rush','scaled_evening']
	create_scores(df,model,cols)
