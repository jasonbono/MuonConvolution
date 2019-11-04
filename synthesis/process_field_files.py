"""
run this script to convert the raw field text files
to a timezone corrected df with ctags, run, subrun,
and other info from the odg
"""

from combine_data_products import pickle_field

#use this as a switch to do systematic studies
make_local_time=False

basedir = "/Users/bono/Desktop/gm2FieldAnalysis/MuonConvolution/"
path = basedir + 'field_info/data/'
files = ['60Hr_Average_Comparison_all_3956_3997_norescut_NoAvg.txt']

for f in files:
    ff = path + f
    print("processing",ff)
    pickle_field(ff,make_local_time=make_local_time)
