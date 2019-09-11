import pandas as pd
import numpy as np
from scipy import ndimage as ndi
from scipy import signal

#from PIL import Image, ImageFilter

def shift_beam(df_input,xshift,yshift):
    '''
        This function translates the 2d beam in x by xshift and y by yshift.
        For values past the physical edges of the beamline (-59 to 59 for both x and y), a wrap-around is used
        
        '''
    #copy the dataframe
    df = df_input.copy()
    
    #hard-code the edges and increments by which to shift (in mm)
    edge = 59
    inc = 2.0
    
    #round the shifts to the nearest 2 mm
    xshift = round(xshift / inc) * inc
    yshift = round(yshift / inc) * inc
    
    # do the x translation
    shift = xshift
    if (shift > 0):
        #limit the size of the shift by wrapping it around the edge boundary
        shift = np.remainder(shift,edge*2.0)
        #bring from zero to the edge
        df['radial'] = df['radial'] + edge
        #do the shift
        df['radial'] = df['radial'] + shift
        #map the values delta + (2*edge + inc) -> delta
        df['radial'] = df['radial'].mod(edge*2.0 + inc)
        #recenter
        df['radial'] = df['radial'] - edge
    else:
        #reverse positive and negative
        df['radial'] = -df['radial']
        shift = -shift
        #limit the size of the shift by wrapping it around the edge boundary
        shift = np.remainder(shift,edge*2.0)
        #bring from zero to the edge
        df['radial'] = df['radial'] + edge
        #do the shift
        df['radial'] = df['radial'] + shift
        #map the values delta + (2*edge + inc) -> delta
        df['radial'] = df['radial'].mod(edge*2.0 + inc)
        #recenter
        df['radial'] = df['radial'] - edge
        #once again, reverse positive and negative
        df['radial'] = -df['radial']
    
    
    # do the y translation
    shift = yshift
    if (shift > 0):
        #limit the size of the shift by wrapping it around the edge boundary
        shift = np.remainder(shift,edge*2.0)
        #bring from zero to the edge
        df['vertical'] = df['vertical'] + edge
        #do the shift
        df['vertical'] = df['vertical'] + shift
        #map the values delta + (2*edge + inc) -> delta
        df['vertical'] = df['vertical'].mod(edge*2.0 + inc)
        #recenter
        df['vertical'] = df['vertical'] - edge
    else:
        #reverse positive and negative
        df['vertical'] = -df['vertical']
        shift = -shift
        #limit the size of the shift by wrapping it around the edge boundary
        shift = np.remainder(shift,edge*2.0)
        #bring from zero to the edge
        df['vertical'] = df['vertical'] + edge
        #do the shift
        df['vertical'] = df['vertical'] + shift
        #map the values delta + (2*edge + inc) -> delta
        df['vertical'] = df['vertical'].mod(edge*2.0 + inc)
        #recenter
        df['vertical'] = df['vertical'] - edge
        #once again, reverse positive and negative
        df['vertical'] = -df['vertical']
    
    
    
    #in keeping with the convention, sort by x, then by y
    #Need to drop the index because operations over rows are done via the index
    df = df.sort_values(['radial','vertical']).reset_index(drop=True)
    
    return df




def add_baseline_noise(df_input,noise_level):

    #copy the dataframe
    df = df_input.copy()
    
    #convert the rel noise level to an abs one
    noise_level = int(noise_level*(df['counts'].mean()))
    
    #add random noise to the counts
    df['counts'] = np.random.randint(noise_level, noise_level+1, df.shape[0]) + df['counts']
    
    #set any negative numbers to zero
    df['counts'][df['counts'] < 0] = 0
    
    return df



def gaus_broadening(df_input,xwidth,ywidth):

    edge = 59
    inc = 2
    gx = np.arange(-3*sigma, 3*sigma, inc)
    gaussian = np.exp(-(x/sigma)**2/2)
    result = np.convolve(original_curve, gaussian, mode="full")



def gaussian_kernel(edge,sigma):
    """Make a 2d gaussian kernel of the specified size (2*edge)
        and sigma.
        
        Both parameters are in mm
        
        The edge should be several times greater than sigma.
        """
    
    edge = np.float128(edge)
    sigma = np.float128(sigma)
    
    #1d positions in 2 mm steps
    pos = np.arange(-edge,edge + 1,2)
    
    #Make a 1d gaussian kernal
    gaus = np.exp(-(pos**2.0)/(2.0*sigma**2.0))
    #normalize to 1
    gaus /= np.sum(gaus)

    #Make the 1d kernel 2d
    kernel = gaus[:, np.newaxis] * gaus[np.newaxis, :]
    kernel = np.float64(kernel)
    
    return kernel





def convolve_df(df,edge,sigma,var='counts'):

    """convolve the dataframe using a gaussian kernel
        
        for now, assumes the dataframe has 60*60 columns
        
        """
    
    #get a 1d array of the 'counts'
    a = df[var].to_numpy()
    #convert to a 2d array
    a = np.reshape(a, (60, 60))
    # get the kernel
    kernel = gaussian_kernel(edge,sigma)
    # do the 2d convolution
    c = ndi.convolve(a,kernel)

    #roll the 2d array back into a 1d array
    c = np.reshape(c, (60*60, -1))
    
    return c



def narrow(df,power,var,new_var):

    original_sum = df[var].sum()
    df[new_var] = df[var]**power
    new_sum = df[new_var].sum()
    df[new_var] = (df[new_var]*original_sum/new_sum).astype(int)
    return df

