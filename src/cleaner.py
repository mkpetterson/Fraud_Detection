# Import Modules
from pprint import pprint
import json
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import re
from typing import List
import pandas as pd
import numpy as np

def re_match_fraud(trg:str) -> bool:
    """ Returns bool if 'fraud' pattern string in target """
    pattern  = re.compile(r'fraud', re.I)
    return bool(pattern.search(trg))

keep = ['channels', 'country', 'currency', 'delivery_method', 'email_domain', 'event_start', 'fb_published', 'has_logo', 'listed', 'payee_name', 'payout_type', 'previous_payouts', 'user_type', 'venue_country', 'venue_latitude', 'venue_longitude']


def clean_with_target(data:any) -> pd.DataFrame:
    """ Returns clean dataframe with wanted columns """
    
    # Create fraud column
    data_cp = data[keep + ['acct_type']].copy()
    data_cp['fraud'] = data_cp['acct_type'].apply(re_match_fraud).astype(int)
    data_cp.drop(columns='acct_type', inplace=True)
    
    # Create other useful features
    data_cp['n_previous_payouts'] = data_cp['previous_payouts'].apply(lambda x: len(x))
    data_cp.drop(columns='previous_payouts', inplace=True)
    
    return data_cp


def clean_row(call:any) -> pd.Series:
    """ Returns clean series with wanted columns, intake taken from Client API call """
    to_keep = ['channels', 'fb_published', 'has_logo', 'user_type', 'n_previous_payouts']
    
    # Put into dataframe
    data_cp = pd.DataFrame(call)
    
    data_cp['n_previous_payouts'] = data_cp['previous_payouts'].apply(lambda x: len(x))
    data_cp.drop(columns='previous_payouts', inplace=True)
       
    cleaned_df = data_cp[to_keep]
    
    return cleaned_df
    
def ohe_existence(data:pd.DataFrame, trg_columns:List[str], rename:bool=True) -> pd.DataFrame:
    """ Given a list of target columns with STR values, function will one-hot-encode column based on the EXISTENCE of the feature """
    data_cop = data.copy()
    
    for col in trg_columns:
        if rename:
            data_cop[f"has_{col}"] = (data_cop[col] != '').astype(int)
            data_cop.drop(columns=col, inplace=True)
        else:
            data_cop[col] = (data_cop[col] == '').astype(int)
            
    return data_cop


    
    
    

    