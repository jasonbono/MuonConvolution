import numpy as np
import pandas as pd



##################
def get_field_df(file):
    df = pd.read_csv(file, sep=" ", header=None)
    df.columns = ["EpochTime", "D", "eD",
                        "NQ", "eNQ","SQ", "eSQ",
                        "NS", "eNS"]
    df['DateTime'] = pd.to_datetime(df['EpochTime'],unit='s')
    df = df.set_index('DateTime')
    del df['EpochTime']
    return df


##################
def field_team_to_standard_moments(b):
    """
        takes in the beam multipole moments in the nominal field teams format and changes
        it to the more universally accepted form ie
        b[0] = c[0],
        b[1] = c[1],
        b[2] = s[1],
        b[3] = c[2],
        b[2] = s[2]
        ...
        
        outputs a numpy array of normal moments (c) and skew moments (s)
        """
    #convert to numpy array
    b = np.array(b)
    #get the number of moments to convert
    N = b.size
    #init c and s, loop over b, and fill accordingly
    c = np.empty(0)
    s = np.empty(0)
    for n in range(N):
        #set the zeroth moments
        if (n==0):
            c = np.append(c,b[n])
            s = np.append(s,0)
        # even numbers in b correspond to skew moments (except zero)
        elif (n%2 == 0):
            s = np.append(s,b[n])
        # odd number is b correspond to normal moments (except zero)
        elif(n%2 != 0):
            c = np.append(c,b[n])

        
    # if b has an odd number of elements, then c will end up one element larger than s
    # fix this by adding zero at the end of the s array
    if (c.size > s.size):
        s = np.append(s,0)
        
    return c,s
