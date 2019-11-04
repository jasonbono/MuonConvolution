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
import pandasql as ps
import os


def pickle_field(file,make_local_time=True):

    #Read the field file and put into a dataframe
    df_field = get_field_df(file)
    #Reset the index
    df_field.reset_index(inplace=True)
    
    #Add the ctags
    df_total = fast_add_ctags(df_field,make_local_time=make_local_time)
    
    
    #the output name is just the input with a different extension
    output = os.path.splitext(file)[0]
    #if you do not correct for timezone, call it a bad offset
    if (make_local_time==False):
        output = output + 'BADOFFSET'
        print("bad offset \n")
    output = output + '.pkl'
    print('saving ' + output)
    #save df as pickle file
    df_total.to_pickle(output)



def fast_add_ctags(df_input,t='DateTime',make_local_time=True):
    """
        This function takes a field df and adds ctag info and other relevant info
        based on an sql join method (for speed)
    """
    
    #Copy the input df as to not manipulate it
    df_field = df_input.copy()
    
    #Ensure the timestamp of the field is in seconds (don't want too much precision)
    df_field[t] = df_field[t].astype('datetime64[s]')
    
    #By default, convert the field's time to chicago time (to match the ODB convention)
    if (make_local_time):
        df_field[t] = df_field[t].dt.tz_localize('utc').dt.tz_convert('US/Central')
    
    #Determine the earliest and latest time in the field dataframe
    start = df_field[t].min()
    end = df_field[t].max()
    
    #Get the ctag Postgres database info within the relevant time interval
    #And put it into a dataframe
    df_ctag = muon_formatter(start=start,end=end)


    #Use the fast method (sql) to join the databases based on overlaping intervals (newer versions of pandas my have self contained solution, but at this point, there is nothing built-in much faster than list comprehention)

    df_total = sql_join(df_field,df_ctag)
    return df_total


def sql_join(df_field,df_ctag):
    """
        Returns a dataframe that joins a field df and an ODB df
        that is indexed by run and subrun number.
        
        It is a faster way, compaired to .apply and list comprehention,
        to combine dataframes based off the criteria of one having a
        value within a range of values from the other
        
        
        WARNING: THIS FUNCTION ASSUMES THE TWO DFS ARE IN THE SAME TIMEZONE
    """

    #define the sql command to join the two dataframes
    sqlcode = '''
    select df_field.*
    ,df_ctag.ctags
    ,df_ctag.run
    ,df_ctag.subrun
    ,df_ctag.start_time
    ,df_ctag.end_time
    ,df_ctag.poor_ctags
    from df_field
    inner join df_ctag
    on df_field.DateTime between df_ctag.start_time and df_ctag.end_time
    '''
    #get the joined dataframe
    df_sql = ps.sqldf(sqlcode,locals())
    #index by run and subrun
    df_sql.set_index(['run','subrun'],inplace=True)
    #reduce the precision of the timestamp to seconds
    df_sql['DateTime'] = df_sql['DateTime'].astype('datetime64[s]')
    df_sql['start_time'] = df_sql['start_time'].astype('datetime64[s]')
    df_sql['end_time'] = df_sql['end_time'].astype('datetime64[s]')
    return df_sql








def field_ctag_dqm(start='2018-04-22 00:00:00',
                   end='2018-04-26 00:00:00',
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
        
        
        WARNING: THIS FUNCTION DOES NOT ACCOUNT FOR TIMEZONE CHANGES
        """
    
    
    #Put the Postgres database info into a dataframe
    df_ctag = muon_formatter(start=start,end=end)
    
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
