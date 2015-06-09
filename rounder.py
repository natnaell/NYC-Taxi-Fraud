import pandas as pd
import gc

'''
This file rounds the coordinates of the trip data to the 3th decimal and
saves a new file with '_r3' at the end.
'''

coord = [ 'pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude']

def round_coord (df):
    for col in coord:
        df[col] = df[col].apply(lambda x: round(x, 3))
        print 'Done with ', col


def read(filename):
        name = '../'+filename
        df = pd.read_csv(name)
        df.columns = [col.strip() for col in df.columns]
        print 'Rounding ', filename, '...'
        round_coord(df)
	df.to_csv(filename[:-4]+'_r3.csv')

def do():
    prefix = 'trip_data_'
    sufix = '.csv'
    #folder = '/media/santiago/2816D26916D23790/Users/Santiago/Documents/taxi/'

    for n in range(1, 13):
        filename = prefix+str(n)+sufix

        print 'Reading ', filename, '...'
        read(filename)
        gc.collect()
        print 'Month '+str(n)+'... Done'

if __name__ == "__main__":
    print 'In...'
    do()
