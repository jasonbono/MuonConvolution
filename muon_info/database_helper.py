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



def muon_formatter(start='2018-04-22 00:00:00',end='2018-04-25 00:00:00'):

    
    
    #read the gm2dq.subrun_time table into a df
    #The start/stop time here is what sets the limits for all subsequent databases
    #which occurs implicitly through the inner joining
    runs = get_runs(start="2018-04-22 00:00:00",end="2018-04-25 00:00:00")
    df_time = pd.DataFrame.from_records(runs,columns=["run", "subrun", "start_time", "end_time"])
    df_time.set_index(['run','subrun'],inplace=True)

    
    #read the gm2dq.ctagswithdqc table into a df
    ctags = get_dqc_ctags()
    df_ctag = pd.DataFrame.from_records(ctags,columns=["run", "subrun", "ctags"])
    df_ctag.set_index(['run','subrun'],inplace=True)

    
    #read the gm2dq.subrun_status table into a df
    flags = get_flags()
    cols = get_labels(table='gm2dq.subrun_status')
    df_flags = pd.DataFrame.from_records(flags,columns=cols)
    df_flags.set_index(['run','subrun'],inplace=True)

    ...



def connect(db='localhost'):
    '''
        establishs a connection to the gm2 online database
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
        
    '''
    
    
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
