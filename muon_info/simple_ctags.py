#Made by Jason Bono, adapted from code from Saskia

import argparse,csv,datetime,time
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import math
import matplotlib.dates as mdate
import psycopg2
from collections import defaultdict
import sys



def get_ctags(start_time, end_time, db='localhost') :

    #connect to the database
    if (db ==  'localhost'):
        dsn  = "dbname=gm2_online_prod user=gm2_writer host=localhost port=5434"
    elif (db == 'g2db-priv'):
        dsn  = "dbname=gm2_online_prod user=gm2_writer host=g2db-priv port=5433"
    else:
        print ("None supported DB specified - run with --db=localhost or --db=g2db-priv")
        sys.exit(-1)
    conn = psycopg2.connect(dsn)
    curr = conn.cursor()


    #get the ctags
    ctag_dict = {}
    sql = "select * from gm2ctag_dqm where time >= '%s' and time <= '%s' order by time DESC" % (start_time, end_time)
    curr.execute(sql)
    conn.commit()
    rows = curr.fetchall()

    for row in rows :
        ct = int(row[1])
        ts = row[0]
        ctag_dict[ts] = ct

    return ctag_dict

