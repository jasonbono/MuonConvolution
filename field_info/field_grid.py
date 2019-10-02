import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

def cartesian_field(b,x,y):
    """
        call with: b an np array of multipole moments of the field in ppm
        x,y a position in space in mm
        
        returns the total magnetic field at the point x,y
        """
    
    #Define R in terms of x and y
    r = np.sqrt(x**2 + y**2)
    R = r/45.0
    #Define theta
    theta = np.arctan2(y,x)
    
    #Add the contribution to the field from the dipole
    field = 0
    field = b[0]
    
    #Add the contribution to the field from the multipole moments
    N = np.size(b)
    #first the normal multipoles
    for n in range(1,math.ceil((N+1)/2.0)):
        field += (R**n)*b[2*n - 1]*np.cos(n*theta)
    #finally the skew multipoles
    for n in range(1,math.ceil((N)/2.0)):
        field += (R**n)*b[2*n]*np.sin(n*theta)
    
    return field





def get_field_grid(b,var='B'):
    """
        Input: the field multipole moments in ppm
        Output: A pandas df with cartesian coordinates the value of the field
    
        Note: The grid is hard-coded to match the grid from the tracker team
        it goes from -59 mm to 59 mm in both x and y in steps of 2 mm
    """

    #get the values of x,y, and B for every point on the grid
    pos = range(-59,60,2)
    vals = [(x,y,cartesian_field(b,x,y)) for x in pos for y in pos]
    vals = np.array(vals)

    #now make a pandas df and fill it with the grid values
    col_names =  ['x', 'y', var]
    df  = pd.DataFrame(columns = col_names)
    df['x'] = vals[:,0]
    df['y'] = vals[:,1]
    df[var] = vals[:,2]
    
    return df



def plot_field(df,bins=60,var='B'):
    fig = plt.figure(figsize=(10, 8))
    plt.hist2d(df['x'], df['y'], weights=df[var], bins=bins,cmap='inferno')
    plt.xlabel('x (mm)')
    plt.ylabel('y (mm)')
    cbar = plt.colorbar()
    cbar.ax.set_ylabel('B Field')
    plt.close()
    return fig
