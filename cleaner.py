import pandas as pd
from points_polygon import *
import gc

def in_manhattan(taxi):
    print 'Removing Outside Manhattan...'
    lista = []
    for x in taxi.index:
        inside = (point_inside_polygon(taxi.pickup_latitude[x], taxi.pickup_longitude[x])) & (point_inside_polygon(taxi.dropoff_latitude[x], taxi.dropoff_longitude[x]))
        lista.append(inside)
    return taxi[lista]

def LatLon_zero (taxi):
    print 'Removing Lat/Long == 0...'
    notzero = (taxi.pickup_latitude != 0) & (taxi.pickup_longitude != 0) & (taxi.dropoff_latitude != 0) & (taxi.dropoff_longitude != 0)
    return taxi[notzero]

def duplicates(taxi):
    print 'Removing Duplicates ... if any'
    taxi.drop_duplicates(inplace=True)

def remove_hack_l(taxi):
    print 'Removing hack_license == 0 ...'
    taxi = taxi[taxi.hack_license != 'CFCD208495D565EF66E7DFF9F98764DA']
    return taxi

def remove_distance_time(taxi):
    print 'Removing ditance<0.3 and time<60s...'
    taxi1 = taxi[taxi.trip_distance>0.3]
    taxi2 = taxi1[taxi1.trip_time_in_secs>60]
    return taxi2

def read(month):
    name = 'taxi_'+str(month)+'.csv'
    print 'Reading Data for Month ', month
    taxi = pd.read_csv(name, index_col=0)
    taxi.columns = [col.strip() for col in taxi.columns]
    print 'Reading ... Done'
    return taxi

def writer(taxi, n):
    outname = 'clean_taxi_'+str(n)+'.csv'
    print 'Writing to file ', outname
    taxi.to_csv(outname, index_label='Index')

def do():

    for n in range(1, 13):
        print 'Cleanning Month ', n, '...'
        taxi = read(n)
        duplicates(taxi)
        taxi = remove_distance_time(taxi)
        taxi = LatLon_zero(taxi)
        taxi = remove_hack_l(taxi)
        taxi = in_manhattan(taxi)

        writer(taxi, n)

        del taxi
        gc.collect()

        print 'Cleaning Month '+str(n)+'... Done'

if __name__ == "__main__":
    print 'In...'
    do()
