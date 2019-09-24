import sys
import numpy as np
import pandas as pd
#muon functions
basedir = "/Users/bono/Desktop/gm2FieldAnalysis/MuonConvolution/"
path = basedir + 'muon_info'
sys.path.append(path)
from database_helper import muon_formatter, time_to_run
from simple_ctags import get_ctags
#field functions
path = basedir + 'field_info/'
sys.path.append(path)
from format_field import get_field_df





def field_ctag_dqm(start='2018-04-22 00:00:00',
                   end='2018-04-25 00:00:00',
                   file="60Hr_Average_Comparison_all_3956_3997_norescut_NoAvg.txt"):
    """
        Returns a dataframe that combines all relevant Postgres database info
        with the field, nominally over the 60 hour dataset, into a dataframe
        indexed by run and subrun number.
        
        In particular, it combines:
        
        *the Postgres ODB's gm2dq.subrun_time table
        *the Postgres ODB's gm2dq.ctagswithdqc
        *the Postgres ODB's gm2dq.subrun_status
        *the Postgres ODB's gm2ctag_dqm (for legacy)
        *the field data product
       
        Can change the arguments of the function to look at data other than the 60 hour dataset
        
        """
    
    
    #Put the Postgres database info into a dataframe
    df_ctag = muon_formatter(start='2018-04-22 00:00:00',end='2018-04-25 00:00:00')
    
    #Put the field info into a dataframe
    path = 'field_info/data/'
    file = basedir + path + file
    df_field = get_field_df(file)
    df_field.reset_index(inplace=True)
    #Add run and subrun columns to the field df and use them as indexes
    times = df_field["DateTime"].tolist()
    l = [time_to_run(t, df_ctag) for t in times]
    df_field['run'] = [v[0][0] for v in l]
    df_field['subrun'] = [v[0][1] for v in l]
    df_field.set_index(['run','subrun'],inplace=True)

    #do an inner join of the two dataframes on the run and subrun indexes
    df_total = pd.merge(df_field, df_ctag, on=['run','subrun'], how='inner')

    return df_total



def field_poor_ctag(start='2018-04-22 00:00:00',
                    end='2018-04-25 00:00:00',
                    file="60Hr_Average_Comparison_all_3956_3997_norescut_NoAvg.txt"):
    """
        Returns a dataframe that combines  info from the Postgres database
        with the field, nominally over the 60 hour dataset, into a dataframe
        indexed time
        
        In particular, it combines:
        
        *the Postgres ODB's gm2ctag_dqm (for legacy)
        *the field data product
        
        Can change the arguments of the function to look at data other than the 60 hour dataset
        
        """
    
    #put the Postgres ODB/muon information into a dataframe
    data = get_ctags("2018-04-22 00:00:00", "2018-04-25 00:00:00",'localhost')
    df_muons = pd.DataFrame.from_dict(data, orient="index",columns=['ctags'])
    df_muons.index.name = 'DateTime'
    df_muons.index = pd.to_datetime(df_muons.index)
    df_muons = df_muons.sort_values(by=['DateTime'])

    #put the field information into a dataframe
    path = 'field_info/data/'
    file = basedir + path + file
    df_field = get_field_df(file)

    #Combine the two dataframes
    #Get the muons/ctag time interval (shorter than the field's time interval)
    muons_time_interval = (df_muons.index.values[1].astype('int64')
                           - df_muons.index.values[0].astype('int64'))//1e9
    #upsample each dataframe to 1 second
    df_muons = df_muons.resample('1S').ffill()
    df_field = df_field.resample('1S').ffill()
    #Join the dataframes
    df_total = df_field.join(df_muons)
    df_total = df_total.fillna(0)
    #calculate ctags per second and add it as a column
    factor = 1/float(muons_time_interval)
    df_total['ctags_per_second'] = df_total['ctags'].astype(float)*factor
    return df_total
