import numpy as np
import pandas as pd

def cartesian_field(b,x,y):
    """
    call with: b an np array of multipole moments of the field in ppm
    x,y a position in space in mm
    
    returns the total magnetic field at the point x,y
    """
    
    x = float(x)
    y = float(y)
    
    #Define R in terms of x and y
    r = np.sqrt(x**2 + y**2)
    R = r/45.0
    #Define theta
    if (y==0):
        theta = 0
    elif ((x==0) and (y>0)):
        theta = np.pi/2
    elif ((x==0) and (y<0)):
        theta = -np.pi/2
    else:
        theta = np.arctan(y/x)

    #Add the contribution to the field from the dipole
    field = b[0]
    #Define the contribution to the field from the odd multipoles
    N = np.size(b)
    #first the odd/normal multipoles
    for n in range(1,N,2):
        field += (R**n)*b[n]*np.cos(n*theta)
    #finally the even/skew multipoles
    for n in range(2,N,2):
        field += (R**n)*b[n]*np.sin(n*theta)

    return field


get_field_grid(b):
    """
        Input: the field multipole moments in ppm
        Output: A pandas df with cartesian coordinates the value of the field
    
        Note: The grid is hard-coded to match the grid from the tracker team
        it goes from -59 mm to 59 mm in both x and y in steps of 1 mm
    """

    #get the values of x,y, and B for every point on the grid
    pos = range(-59,60)
    vals = [(x,y,cartesian_field(a,x,y)) for x in pos for y in pos]
    vals = np.array(vals)

    #now make a pandas df and fill it with the grid values
    col_names =  ['x', 'y', 'B']
    df  = pd.DataFrame(columns = col_names)
    df['x'] = vals[:,0]
    df['y'] = vals[:,1]
    df['B'] = vals[:,2]
    df['B'].apply((lambda x: x + cartesian_field(a,0,0)))
    return df

