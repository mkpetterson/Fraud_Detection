# Import Modules
from pprint import pprint
import json
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import re
from typing import List
import pandas as pd
import numpy as np

# Import for Country Related Parsing
import pycountry


'''GLOBAL'''

keep = ['channels', 'country', 'currency', 'delivery_method', 'email_domain', 'event_start', 'fb_published', 'has_logo', 'listed', 'payee_name', 'payout_type', 'previous_payouts', 'user_type', 'venue_country', 'venue_latitude', 'venue_longitude']


'''DF CLEANING'''

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

'''ENCODING'''

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


'''PARSING'''

def re_match_fraud(trg:str, to_match:str='fraud') -> bool:
    """ Returns bool if 'fraud' pattern string in target, set to_match var for another match """
    pattern  = re.compile(f'{to_match}', re.I)
    return bool(pattern.search(trg))

def get_country_code(alpha_2:str, cast_int:bool=True) -> int:
    """ Returns ISO-3166 Country code from given country abbreviation """
    res = -1
    try:
        res = pycountry.countries.get(alpha_2=alpha_2).numeric
        if cast_int:
            res = int(res)
    except:
        pass
    return res

def get_currency_code(alpha_3:str, cast_int:bool=True) -> int:
    """ Returns ISO-4217 Country code from given country abbreviation """
    res = -1
    try:
        res = pycountry.currencies.get(alpha_3=alpha_3).numeric
        if cast_int:
            res = int(res)
    except:
        pass
    return res
    
    
    

    