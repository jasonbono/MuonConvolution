
import pandas as pd
def get_field_df(file):


    df = pd.read_csv(file, sep=" ", header=None)
    df.columns = ["EpochTime", "D", "eD",
                        "NQ", "eNQ","SQ", "eSQ",
                        "NS", "eNS"]
    df['DateTime'] = pd.to_datetime(df['EpochTime'],unit='s')
    df = df.set_index('DateTime')
    del df['EpochTime']
    return df
