'''
This programs combines the trip data and the fare data in only 1 file, that
has all of the trip data and the last 7 columns of the fare file ('fare_col' list)
'''

import pandas as pd
import gc

fare_col = ['payment_type',
 'fare_amount',
 'surcharge',
 'mta_tax',
 'tip_amount',
 'tolls_amount',
 'total_amount']

def read(month):
    trip_name = 'trip_data_'+str(month)+'_r3.csv'
    fare_name = '../trip_fare_'+str(month)+'.csv'
    print 'Reading Trip Data for Month ', month
    trip = pd.read_csv(trip_name)
    trip.columns = [col.strip() for col in trip.columns]
    print 'Reading Fare Data for Month ', month
    fare = pd.read_csv(fare_name)
    fare.columns = [col.strip() for col in fare.columns]
    print 'Reading ... Done'
    return trip, fare

def combine(trip, fare):
    print 'Combining both Files...'
    taxi = pd.concat([trip, fare[fare_col]], axis=1)
    return taxi

def writer(taxi, n):
    outname = 'taxi_'+str(n)+'.csv'
    print 'Writing to file ', outname
    taxi.to_csv(outname, index_label='Index')

def do():

    for n in range(1, 13):

        trip, fare = read(n)

        taxi = combine(trip, fare)

        del trip
        del fare
        gc.collect()

        writer(taxi, n)

        del taxi
        gc.collect()

        print 'Combining Month '+str(n)+'... Done'

if __name__ == "__main__":
    print 'In...'
    do()
