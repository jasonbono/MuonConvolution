import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



##############################
def get_distribution_moments(N,x,y,weights):
    
    """Returns the unnormalized 'distribution moments'
        lumped into two np arrays: one for the normal moments, the other for skew
        Theese moments are the numerator in the evaluation of the standard multipole moments
        """
    
    
    #Define the zeroth moment
    #ie the normalization factor
    #in the probability dencity function
    I_zero = weights.sum()
    
    #define the 'normal' distribution moments
    def I(n):
        if n==0:
            return I_zero
        else:
            r = np.sqrt(x**2 + y**2)
            r = r/45.0
            theta = np.arctan2(y,x)
            cos = np.cos(n*theta)
            raw = (weights*(r**n)*cos).sum()
            return raw

    #define the 'skew' distribution moments
    def J(n):
        if n==0:
            return 0
        else:
            r = np.sqrt(x**2 + y**2)
            r = r/45.0
            theta = np.arctan2(y,x)
            sin = np.sin(n*theta)
            raw = (weights*(r**n)*sin).sum()
            return raw

    I_vals = np.array([I(n) for n in range(N)])
    J_vals = np.array([J(n) for n in range(N)])
    return I_vals,J_vals




##############################
def get_normalized_distribution_moments(N,x,y,weights):
    
    """Returns the normalized 'distribution moments'
        lumped into two np arrays: one for the normal moments, the other for skew
        Theese moments can be used directly as an averager of another field
        eg in <B> = BXM where M are the moments return in this distribution and B is represented
        in the expansion into multipole moments
        """
    #Get the raw distribution moments
    I_vals,J_vals = get_distribution_moments(N,x,y,weights)
    #Normalize them
    I_norm_vals = I_vals/I_vals[0]
    J_norm_vals = J_vals/I_vals[0]

    return I_norm_vals,J_norm_vals








##############################
def get_spacial_moments(N,x,y,weights):
    
    """Returns the 'spacial moments'
        lumped into two np arrays: one for the normal moments, the other for skew
        Theese moments are the denominator in the evaluation of the standard multipole moments
        """
    
    
    #Define the zeroth moment
    #ie the total area, which is just the number of squares counted
    Psi_zero = weights.count()
    
    #define the 'normal' spacial moments
    def Psi(n):
        if n==0:
            return Psi_zero
        else:
            r = np.sqrt(x**2 + y**2)
            r = r/45.0
            theta = np.arctan2(y,x)
            cos = np.cos(n*theta)
            raw = ((r**(2*n))*cos**2).sum()
            return raw

    #define the 'skew' distribution moments
    def Omega(n):
        if n==0:
            return 0
        else:
            r = np.sqrt(x**2 + y**2)
            r = r/45.0
            theta = np.arctan2(y,x)
            sin = np.sin(n*theta)
            raw = ((r**(2*n))*sin**2).sum()
            return raw

    Psi_vals = np.array([Psi(n) for n in range(N)])
    Omega_vals = np.array([Omega(n) for n in range(N)])
    return Psi_vals,Omega_vals





##############################
def get_multipole_moments(N,x,y,weights):
    
    """Returns the standard multipole moments
        lumped into two np arrays: one for the normal moments, the other for skew
        """
    
    #Get the "distribution moments"
    I_vals,J_vals = get_distribution_moments(N,x,y,weights)
    
    #Get the "spacial moments"
    Psi_vals,Omega_vals = get_spacial_moments(N,x,y,weights)
    
    C_vals = I_vals/Psi_vals
    S_vals = np.zeros(N)
    S_vals[0] = 0
    S_vals[1:] = J_vals[1:]/Omega_vals[1:]
    
    return C_vals,S_vals








##############################
def get_df_tracker(file = "/Users/bono/Desktop/gm2FieldAnalysis/MuonConvolution/tracker_info/sample_data/beamSpot.txt", correct_offset=False):
    
    """
    This function takes in a text file provided by the tracker team and returns a dataframe that represents a histogram of the beam as seen by the tracker
    
    The radial and vertical positions are in mm. There are two stations, so the dataframe has a station column
    
    The option to correct offset corrects for the radial tangency offset (see saskia's thesis, page 125)
    
    """
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
    
    
    #optionally, apply the radial offset (hardcoded number in mm,  based on Saskia's Thesis, page 126)
    if(apply_offset==True):
        df["radial"] = df["radial"] - 1.09
    
    #reset the index
    df.reset_index(inplace=True)
    
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




def plot_beam(df,bins=60,var='counts'):
    fig = plt.figure(figsize=(10, 8))
    plt.hist2d(df['radial'], df['vertical'], weights=df[var], bins=bins,cmap='inferno')
    plt.xlabel('radial (mm)')
    plt.ylabel('vertical (mm)')
    plt.xlabel('radial (mm)',fontsize=18)
    plt.ylabel('vertical (mm)',fontsize=18)
    plt.xlim((-59, 59))
    plt.ylim((-59, 59))
    
    cbar = plt.colorbar()
    cbar.ax.set_ylabel(var)
    plt.close()
    
    return fig






