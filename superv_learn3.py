import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, BaggingRegressor
import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from sklearn.preprocessing import scale

def knn(df1, features, pred_var, df2):
    cl = KNeighborsRegressor(n_neighbors=3)
    cl.fit(df1[features], df1[pred_var])
    print 'KNN Score: ', cl.score(df2[features], df2[pred_var])
    #return lr

def linear_reg(df1, features, pred_var, df2):
    lr = LinearRegression(normalize=True)
    lr.fit(df1[features], df1[pred_var])
    print 'Linear Reg Score: ', lr.score(df2[features], df2[pred_var])
    return lr.predict(df2[features])

def log_reg(df1, features, pred_var, df2):
    lr = LogisticRegression()
    lr.fit(df1[features], df1[pred_var])
    print 'Log Reg Score: ', lr.score(df2[features], df2[pred_var])
    #return lr.predict(df2[features])

def linearSVN(df1, features, pred_var, df2):
    lr = linearSVC()
    lr.fit(df1[features], df1[pred_var])
    print 'SVN Score: ', lr.score(df2[features], df2[pred_var])
    #return lr.predict(df2[features])

def tree(df1, features, pred_var, df2):
    cl = DecisionTreeRegressor()
    cl.fit(df1[features], df1[pred_var])
    print 'Tree Score: ', cl.score(df2[features], df2[pred_var])


def random_forest(df1, features, pred_var, df2):
    lr = RandomForestRegressor()
    lr.fit(df1[features], df1[pred_var])
    print 'Rand Forest Score: ', lr.score(df2[features], df2[pred_var])
    #return lr.predict(df2[features])


def boosting(df1, features, pred_var, df2):
    #for x in [10, 100, 1000]:
	#for y in [3, 5, 7]:
    lr = GradientBoostingRegressor(n_estimators=100, max_depth=7)
    lr.fit(df1[features], df1[pred_var])
    print 'GradientBoostingRegressor Score: ',  lr.score(df2[features], df2[pred_var])
    #0.727261516253
    return lr.predict(df2[features])


def bagging(df1, features, pred_var, df2):
    lr = BaggingRegressor()
    lr.fit(df1[features], df1[pred_var])
    print 'BaggingClassifier Score: ', lr.score(df2[features], df2[pred_var])
    #return lr.predict(df2[features])

def show(df, features, pred_var, reg):

    plt.scatter(df[features[0]], df[pred_var], color='black')
    plt.plot(df[features[0]], reg.predict(df[pred_var]), color='blue', linewidth=2)
    plt.title('Time')
    plt.xticks(())
    plt.yticks(())
    plt.savefig('linear_regression1.png')

    plt.scatter(df[features[1]], df[pred_var], color='green')
    plt.plot(df[features[1]], reg.predict(df[pred_var]), color='red', linewidth=2)
    plt.title('Distance')
    plt.xticks(())
    plt.yticks(())
    plt.savefig('linear_regression2.png')

def read(month):
    name = 'clean_taxi_'+str(month)+'.csv'
    print 'Reading Data for Month ', month
    df = pd.read_csv(name, index_col=0)
    df.columns = [col.strip() for col in df.columns]
    #df['pickup_dt'] = pd.to_datetime(df['pickup_datetime'])
    #df['dow'] = df['pickup_dt'].dt.dayofweek

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


    print 'Reading ... Done'
    return df

def do():
    df1 = read(9)
    df2 = read(10)
    features = ['trip_time_in_secs', 'trip_distance', 'dow']
    pred_var = 'fare_amount'
    cols = ['scaled_weekend','scaled_passenger_count','scaled_pickup_latitude','scaled_pickup_longitude','scaled_dropoff_latitude','scaled_dropoff_longitude','scaled_morning','scaled_afternoon','scaled_rush','scaled_evening']


    #for x in features:
        #linear_reg(df, [x], pred_var)
    #predicted = linear_reg (df1, features, pred_var, df2)

    #knn (df1, [features[0], features[1]], pred_var, df2)
    #tree (df1, [features[0], features[1]], pred_var, df2)

    #random_forest (df1, [features[0], features[1]], pred_var, df2)

    #bagging (df1, [features[0], features[1]], pred_var, df2)
    #linearSVN (df1, [features[0], features[1]], pred_var, df2)
    #log_reg (df1, [features[0], features[1]], pred_var, df2)


    #linear_reg (df, features, pred_var)
    #show(df, features, pred_var, reg)

    predicted = boosting (df1, cols, pred_var, df2)

    df2['predict_fare'] = predicted
    df2['difference'] = df2.fare_amount - df2.predict_fare
    df2 = df2[abs(df2['difference'])<=100]
    driver_scores=pd.DataFrame(df2.groupby(['hack_license'])['difference'].sum() , copy = True)

    driver_scores['normal_prob'] = np.apply_along_axis( norm.cdf, 0, scale( driver_scores['difference'] ) )
    driver_scores.to_csv('driver_score_clean_boosting_final.csv')
    df2[['predict_fare', 'difference']].to_csv('ride_score_clean_boosting_final.csv')





if __name__ == "__main__":
    print 'In...'
    do()
