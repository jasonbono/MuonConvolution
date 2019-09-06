import pandas as pd
import numpy as np
import matplotlib.pyplot as plt




def get_df_tracker(file = "/Users/bono/Desktop/gm2FieldAnalysis/MuonConvolution/tracker_info/sample_data/beamSpot.txt"):
    names=['radial', 'vertical', 'counts']
    df = pd.read_csv(file, sep=" ",names=names)
    df.index.name = 'index'
    #Make a 'Station' column to keep a record of where the readings came from
    sub ='station'
    mask = df["vertical"].str.find(sub) != -1
    df[mask]
    df['Station'] = df[mask]['vertical']
    df['Station'] = df['Station'].fillna(method='ffill')
    df.head()

    #clean the data by removing all rows with values that can not be interpreted numerially
    df = df[pd.to_numeric(df['radial'], errors='coerce').notnull()]

    #convert values to ints
    df["counts"] = df["counts"].astype('float')
    df["radial"] = df["radial"].astype('float')
    df["vertical"] = df["vertical"].astype('float')

    return df


def get_mean(vals,weights):
    '''
    
    returns the weighted (scalar) mean
    '''
    ans = (vals*weights).sum()/weights.sum()
    return ans


def get_rms(vals,mean,weights):
    '''
    vals and weights are a pd.series
    mean is a scalar
    
    returns the weighted (scalar) varience
    '''
    ans = (weights*(vals - mean)**2).sum()/weights.sum()
    ans = np.sqrt(ans)
    return ans




def get_2dhist_tracker(df,bins=100):
    x = df["radial"]
    y = df["vertical"]
    w = df["counts"]
    H, xedges, yedges = np.histogram2d(x, y, weights=w, bins=bins)
    return H.T,xedges,yedges




def plot_beam(df,bins=60):
    fig = plt.figure(figsize=(10, 8))
    plt.hist2d(df['radial'], df['vertical'], weights=df['counts'], bins=bins,cmap='inferno')
    plt.xlabel('radial (mm)')
    plt.ylabel('vertical (mm)')
    plt.xlim((-59, 59))
    plt.ylim((-59, 59))
    
    cbar = plt.colorbar()
    cbar.ax.set_ylabel('Counts')
    plt.close()
    
    return fig
