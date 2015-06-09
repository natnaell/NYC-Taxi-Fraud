""" This module can be used to create plots of the distribution of fares/distances/times by hour of the day or day of the week

"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

days = {1:'Monday',
        2:'Tuesday',
        3:'Wednesday',
        4:'Thursday',
        5:'Friday',
        6:'Saturday',
        7:'Sunday'}

labels = {'fare_amount':'Fare Amount ($)',
            'trip_distance':'Trip Distance (mi)',
            'trip_time_in_secs':'Trip Time (s)'}

def plot_hours(df, col, save=True, figdir=''):
    
    fig, ax = plt.subplots(8, 3, figsize=(16,12))
    #plt.subplots_adjust(hspace=0.3)
    
    #col = 'fare_amount'
    
    gcol = 'hour_of_day'
    
    if col == 'fare_amount': xmax, bins = 30, 60
    elif col == 'trip_distance': xmax, bins = 10, 20
    elif col == 'trip_time_in_secs': xmax, bins = 3000, 50
    else: xmax, bins = df[col].max(), 10    

    mx = 0
    n = 24
    
    for h in range(n):
        y, _ = np.histogram(df.ix[df[gcol] == h, col], bins=bins, range=(0,xmax))
        if max(y) > mx:
            mx = max(y)
    ymax = mx + (500 - mx) % 500
    
    for h in range(n):
        r = h % 8
        c = h / 8
        ix = df[gcol] == h
        s = df.ix[ix, col]
        s.hist(ax=ax[r,c], bins=bins, range=(0,xmax), color='#cccccc', grid=False)
        ax[r,c].set_ylim(0,ymax)
        ax[r,c].text(xmax*0.7, ymax*0.75, '{}:00 - {}:00'.format(h,h+1))
        ax[r,c].spines['top'].set_visible(False)
        ax[r,c].spines['right'].set_visible(False)
        ax[r,c].get_xaxis().tick_bottom()  
        ax[r,c].get_yaxis().tick_left()
        ax[r,c].set_xlabel(labels[col])
        
    if save: plt.savefig(figdir + col + '_hours.png', bbox_inches='tight')
    else: return fig, ax
    
def plot_days(df, col, save=True, figdir=''):
    
    fig, ax = plt.subplots(1, 7, figsize=(16,1))
    plt.subplots_adjust(wspace=0.4)
    
    #col = 'fare_amount'
    
    gcol = 'day_of_week'

    if col == 'fare_amount': xmax, bins = 30, 60
    elif col == 'trip_distance': xmax, bins = 10, 20
    elif col == 'trip_time_in_secs': xmax, bins = 3000, 50
    else: xmax, bins = df[col].max(), 10 
    
    mx = 0
    n = 7
    
    for h in range(n):
        y, _ = np.histogram(df.ix[df[gcol] == h, col], bins=bins, range=(0,xmax))
        if max(y) > mx:
            mx = max(y)
    ymax = mx + (500 - mx) % 500
    
    for i in range(n):
        
        ix = df[gcol] == i+1
        
        s = df.ix[ix, col]
        s.hist(ax=ax[i], bins=bins, range=(0,xmax), color='#cccccc', grid=False)
        ax[i].set_ylim(0,ymax)
        ax[i].set_title(days[i+1])
        ax[i].spines['top'].set_visible(False)
        ax[i].spines['right'].set_visible(False)
        ax[i].get_xaxis().tick_bottom()  
        ax[i].get_yaxis().tick_left()
        ax[i].set_xlabel(labels[col])
    
    if save: plt.savefig(figdir + col + '_days.png', bbox_inches='tight')
    else: return fig, ax
    
def plot_days_same(df, col, save=True, figdir=''):
    
    fig, ax = plt.subplots(1, 1, figsize=(12,9))
    
    #col = 'fare_amount'
    
    gcol = 'day_of_week'
    
    if col == 'fare_amount': xmax, bins = 30, 60
    elif col == 'trip_distance': xmax, bins = 10, 20
    elif col == 'trip_time_in_secs': xmax, bins = 3000, 50
    else: xmax, bins = df[col].max(), 10 

    mx = 0
    n = 7
    color=iter(matplotlib.cm.rainbow(np.linspace(0,1,n)))
    
    for i in range(n):
    
        ix = df[gcol] == i + 1
        
        s = df.ix[ix, col]
        y, x = np.histogram(s, bins=bins, range=(0,xmax))
        if max(y) > mx:
            mx = max(y)
        ax.plot(x[1:], y, color=next(color), label=days[i+1], lw=2.)
    
    ymax = mx + (500 - mx) % 500
    ax.set_ylim(0,ymax)
    ax.set_title('Days of Week')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()  
    ax.get_yaxis().tick_left()
    ax.set_xlabel(labels[col])
    ax.grid(False)
    ax.legend()

    if save: plt.savefig(figdir + col + '_days1.png', bbox_inches='tight')
    else: return fig, ax
