"""
run this script to convert the raw field text files
to a timezone corrected df with ctags, run, subrun,
and other info from the odg

Warning: This script calls a function that can only run if you have a connection
to the odb! make sure to kinit and open the appropriate connection!
"""

from combine_data_products import pickle_field



basedir = "/Users/bono/Desktop/gm2FieldAnalysis/MuonConvolution/"

#for the original 60 hour dataset
#n_multipoles = 4
#path = basedir + 'field_info/data/'
#files = ['60Hr_Average_Comparison_all_3956_3997_norescut_NoAvg.txt']

#for all the data with updated uncertainties but a cutoff
#at the NS
#n_multipoles = 4
#path = basedir + 'field_info/data/run1/limited_multipoles/'
#files = ['60Hr_Average_Comparison_all_3956_3997_norescut_NoAvg_both.txt',
#'9day_Average_Comparison_all_4138_4181_norescut_NoAvg_both.txt',
#'9day_Average_Comparison_all_4189_4226_norescut_NoAvg_both.txt',
#'9day_Average_Comparison_all_4226_4265_norescut_NoAvg_both.txt',
#'9day_Average_Comparison_all_4265_4493_norescut_NoAvg_both.txt',
#'endgame_Average_Comparison_all_5054_5103_norescut_NoAvg_both.txt',
#'endgame_Average_Comparison_all_5117_5157_norescut_NoAvg_both.txt',
#'endgame_Average_Comparison_all_5169_5217_norescut_NoAvg_both.txt',
#'endgame_Average_Comparison_all_5217_5259_norescut_NoAvg_both.txt',
#'HighKick_Average_Comparison_all_4058_4098_norescut_NoAvg_both.txt',
#'HighKick_Average_Comparison_all_4098_4138_norescut_NoAvg_both.txt'
#]


#for the first try at updated error and all the multipoles (up to NO)
n_multipoles = 9
path = basedir + 'field_info/data/run1/all_multipoles/run1_v00/'
files = ['60Hr_vals_uncertainties_3956-3997.txt',
'9day_vals_uncertainties_4138-4181.txt',
'9day_vals_uncertainties_4226-4265.txt',
'9day_vals_uncertainties_4265-4493.txt',
#'HighKick_vals_uncertainties_4058-4098.txt',
#'HighKick_vals_uncertainties_4098-4138.txt',
'endgame_vals_uncertainties_5054-5103.txt',
'endgame_vals_uncertainties_5117-5157.txt',
'endgame_vals_uncertainties_5169-5217.txt',
'endgame_vals_uncertainties_5217-5259.txt'
]

files = ['HighKick_vals_uncertainties_4058-4098.txt',
'HighKick_vals_uncertainties_4098-4138.txt'
]



#use this as a switch to do systematic studies
make_local_time=True



for f in files:
    ff = path + f
    print("processing",ff)
    pickle_field(ff, make_local_time=make_local_time, n_multipoles=n_multipoles)
