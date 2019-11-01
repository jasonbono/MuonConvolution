import pandas as pd
import argparse,csv,datetime,time
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import math
import matplotlib.dates as mdate
import psycopg2
from collections import defaultdict
import sys



def muon_formatter(start='2018-04-22 00:00:00',end='2018-04-26 00:00:00'):
    
    #convert start and end time to string
    start = str(start)
    end = str(end)
    
    
    #Read the gm2dq.subrun_time table into a df
    #The start/stop time here is what sets the limits for all subsequent databases
    #which occurs implicitly through the inner joining
    runs = get_runs(start=start,end=end)
    df_time = pd.DataFrame.from_records(runs,columns=["run", "subrun", "start_time", "end_time"])
    df_time.set_index(['run','subrun'],inplace=True)
    
    #Read the gm2dq.ctagswithdqc table into a df
    ctags = get_dqc_ctags()
    df_ctag = pd.DataFrame.from_records(ctags,columns=["run", "subrun", "ctags"])
    df_ctag.set_index(['run','subrun'],inplace=True)

    #Read the gm2dq.subrun_status table into a df
    flags = get_flags()
    cols = get_labels(table='gm2dq.subrun_status')
    df_flags = pd.DataFrame.from_records(flags,columns=cols)
    df_flags.set_index(['run','subrun'],inplace=True)

    
    #Do an inner join to get a df with all relevant information from the database
    df_total = pd.merge(df_time, df_ctag, on=['run','subrun'], how='inner')
    df_total = pd.merge(df_total, df_flags, on=['run','subrun'], how='inner')
    
    
    #Read the gm2ctag_dqm table into a df
    poor = get_poor_ctags(start=start,end=end)
    df_poor = pd.DataFrame.from_records(poor,columns=["poor_time", "poor_ctags"])
    #get runs/subruns for the df of gm2ctag_dqm
    times = df_poor['poor_time'].tolist()
    l = [time_to_run(t, df_total) for t in times]
    df_poor['run'] = [v[0][0] for v in l]
    df_poor['subrun'] = [v[0][1] for v in l]
    df_poor.set_index(['run','subrun'],inplace=True)

    #Do another inner join 
    df_total = pd.merge(df_total, df_poor, on=['run','subrun'], how='inner')

    return df_total



def connect(db='localhost'):
    '''
        establishes a connection to the gm2 online database
    '''
    
    if (db ==  'localhost'):
        dsn  = "dbname=gm2_online_prod user=gm2_writer host=localhost port=5434"
    elif (db == 'g2db-priv'):
        dsn  = "dbname=gm2_online_prod user=gm2_writer host=g2db-priv port=5433"
    else:
        print ("None supported DB specified - run with --db=localhost or --db=g2db-priv")
        sys.exit(-1)
    conn = psycopg2.connect(dsn)
    curr = conn.cursor()
    return conn,curr


def get_labels(db='localhost', table='') :
    '''
        returns column names for the tables in the gm2 online database
    '''
    
    #connect
    conn,curr = connect(db)
    
    #get the column names for the specified table
    sql = "SELECT * FROM " + table +  " LIMIT 0"
    curr.execute(sql)
    colnames = [desc[0] for desc in curr.description]
    
    #close the connection without commiting any accidential changes
    conn.rollback()
    
    return colnames



def get_runs(start, end, db='localhost', table='gm2dq.subrun_time'):
    '''
        takes in a user specified start and end time as a range
        
        returns all run, subrun, start_time (for the subrun),
        and end_time (for the run) within the specified time range
        for (nominally) the gm2dq.subrun_time table
       
       note: the DQC is in chicago time, but rachel's field product is in UTC
    '''
    
    
    #convert start and end time to string
    start = str(start)
    end = str(end)
    
    #connect
    conn,curr = connect(db)
    
    #Prepare the sql command and execute
    what = f"select run, subrun, start_time, end_time from {table} "
    where = f"where start_time >= '{start}' and end_time <= '{end}' "
    order = "order by start_time ASC"
    sql = what + where + order
    curr.execute(sql)
    
    #fetch the data
    rows = curr.fetchall()
    
    #Close the connection without commiting any accidential changes
    conn.rollback()
    
    return rows




def get_dqc_ctags(db='localhost', table='gm2dq.ctagswithdqc'):
    
    '''
        nominally for the gm2dq.ctagswithdqc table
        
        returns all run, subrun, and ctags values
        stored in the entire database (eg beyond the 60 hour dataset)
    '''
    
    #connect
    conn,curr = connect(db)
    
    #Prepare the sql command and execute
    what = f"select run, subrun, ctags from {table} "
    order = "order by run,subrun ASC"
    sql = what + order
    curr.execute(sql)
    
    #fetch the data
    rows = curr.fetchall()
    
    #Close the connection without commiting any accidential changes
    conn.rollback()
    
    return rows



def get_flags(db='localhost', table='gm2dq.subrun_status'):
    
    '''
        nominally for the gm2dq.subrun_status table
        
        returns a large number of quality flags
        stored in the entire database (eg beyond the 60 hour dataset)
        '''
    
    
    #connect
    conn,curr = connect(db)
    
    #Prepare the sql command and execute
    what = f"select * from {table} "
    order = "order by run,subrun ASC"
    sql = what + order
    curr.execute(sql)
    
    #fetch the data
    rows = curr.fetchall()
    
    #Close the connection without commiting any accidential changes
    conn.rollback()
    
    return rows




def get_poor_ctags(start,end, db='localhost', table='gm2ctag_dqm') :
    
    '''
        takes in a user specified start and end time as a range
        nominally for the gm2ctag_dqm table
        
        returns the time and ctag values for times within the specified interval
    '''
    
    
    #convert start and end time to string
    start = str(start)
    end = str(end)
    
    #connect
    conn,curr = connect(db)
    
    #Prepare the sql command and execute
    what = f"select time, ctags from {table} "
    where = f"where time >= '{start}' and time <= '{end}' "
    order = "order by time ASC"
    sql = what + where + order
    curr.execute(sql)
    conn.commit()
    
    #fetch the data
    rows = curr.fetchall()
    
    return rows




def time_to_run(time,df):
    
    """
        this is a function that returns a run/subrun based off a time
        it takes in a specific time and a dataframe
        the time is searched for in the dataframe which is assumed to have runs/subruns associated with times in each of the dataframe's rows
        
        it returns a run/subrun based off the time
        
    """
    
    #Convert to date/time
    time = pd.to_datetime(time)
    
    #select only the rows that span the specified time
    mask =  (time >  df['start_time']) & (time <=  df['end_time'])
    
    #Get the list of tuples of the runs/subruns
    ans = df[mask].index.tolist()
    
    #if the list is empty, set the run and subrun to -1
    if (ans == []):
        ans = [(-1,-1)]
    
    return ans
