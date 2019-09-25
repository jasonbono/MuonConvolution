import numpy as np

#setup the base dir
basedir='/Users/bono/Desktop/gm2FieldAnalysis/MuonConvolution/'

#import the relevant beam moments functions
import sys
path = basedir + 'tracker_info'
sys.path.insert(0,path)
from beam_moments import get_normalized_distribution_moments as gndm





def moments_method(c,s,I_norm,J_norm):
    """
        takes in the beam multipole moments in the
        world standard format (ie c and s for normal and skew)
        
        It then takes in the normalized beam "distribution moments" I_norm and J_norm
        
        It returns the average of the field B, as described by B, weighted by the muons, as described by I_norm and J_norm
        
        """
    #the normal components (c0*1 + Sum_{n=1} c[n]*I[n]/I[0])
    B = np.sum(c*I_norm)
    #the skew components (0*0 + Sum_{n=1} s[n]*J[n]/J[0])
    B += np.sum(s*J_norm)
    return B
