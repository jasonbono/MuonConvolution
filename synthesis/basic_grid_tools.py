import pandas as pd
import numpy as np
import matplotlib as plt
import matplotlib.pyplot as plt

def get_avg_val(df,x,y,width,xvar='x',yvar='y',zvar='acc'):
    """
    This function takes in a dataframe with a 2d histogram structure (xvar,yvar,zvar)
    and a point in the 2d grid (x,y).
    It computes a z value at x and y, based on the mean value of zvar in the surrounding space

    Notes: The size of the neighborhood is specified (width).
    if width is too small for the input df, such that any value of x,y can fall between the grid points,
    then width is increased to match the input grid spacing
    """
    #ensure the search width is positive
    width = abs(width)

    #dont want to fall inbetween the cracks
    #find the spacing of the grid of the input df
    width_lim = abs(df.x.unique()[0] - df.x.unique()[1])/2.0
    #if the specified width is less than limit, set the former equal to the latter
    if (width<width_lim):
        width=width_lim

    #define the search region
    mask = (df[xvar] <= (x + width)) & (df[xvar] >= (x - width)) & (df[yvar] <= (y + width)) & (df[yvar] >= (y - width))
    df_region = df.copy()
    df_region = df_region[mask]

    #get the average value of var within the search region
    z = df_region[zvar].mean()

    return z




def rebin_df(df,edge=59,step=0.5,xvar='x',yvar='y',zvar='acc'):

    #get the values of x,y, and B for every point on the grid
    pos = np.arange(-edge,edge+1,step)
    vals = [(x,y,get_avg_val(df,x,y,step,xvar=xvar,yvar=yvar,zvar=zvar)) for x in pos for y in pos]
    vals = np.array(vals)

    #now make a pandas df and fill it with the grid values
    col_names =  [xvar, yvar, zvar]
    new_df  = pd.DataFrame(columns = col_names)
    new_df['x'] = vals[:,0]
    new_df['y'] = vals[:,1]
    new_df[zvar] = vals[:,2]

    #force float type
    new_df[xvar] = new_df[xvar].astype('float')
    new_df[yvar] = new_df[yvar].astype('float')
    new_df[zvar] = new_df[zvar].astype('float')

    return new_df



def plot_grid(df,xvar='x',yvar='y',zvar='acc'):
    #get the number of xbins/ybins (assumes square grid)
    bins = df[xvar].nunique()
    
    fig = plt.figure(figsize=(10, 8))
    plt.hist2d(df[xvar], df[yvar], weights=df[zvar], bins=bins,cmap='inferno')
    plt.xlabel(xvar)
    plt.ylabel(yvar)
    cbar = plt.colorbar()
    cbar.ax.set_ylabel(zvar)
    plt.close()
    return fig
