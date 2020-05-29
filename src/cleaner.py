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

keep = ['channels', 'country', 'currency', 'delivery_method', 'email_domain', 'event_created', 'event_published', 'event_end', 'event_start', 'fb_published', 'has_logo', 'listed', 'payee_name', 'payout_type', 'previous_payouts', 'user_created', 'user_type', 'venue_country', 'venue_latitude', 'venue_longitude']


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
    
    
    data_cp['payout_type'] = data_cp['payout_type'].apply(lambda x: 1 if x=='ACH' else 2 if x=='CHECK' else 3)
    data_cp['listed'] = data_cp['listed'].apply(lambda x: 1 if x=='y' else 0)
    
    # Change country, venue country, and currency
    for col in ['country', 'venue_country', 'currency']:
        method = get_country_code if re_match_fraud(col, 'country') else get_currency_code
        data_cp[col] = data_cp[col].apply(method)
    
    data_cp = create_features(data_cp)
    
    
    return data_cp


def create_features(data:pd.DataFrame) -> pd.DataFrame:
    """ Creates features from given data geared towards KNN Model """
    res = data.copy()

    res['country'] = res['country'].fillna('None')
    
    # Durations (create durations between event_created/start/end/publish)
    res['event_duration'] = res['event_end'] - res['event_start']
    res['event_till_publish'] = res['event_published'] - res['event_created']
    res['user_event_lifespan'] = res['event_created'] - res['user_created']
    res.drop(columns=['event_created', 'event_published', 'event_start', 'event_end'], inplace=True)
    
    return res



def clean_row(call:any, drop_cord:bool=True) -> pd.Series:
    """ Returns clean series with wanted columns, intake taken from Client API call """
    keep = ['channels', 'country', 'currency', 'delivery_method', 'email_domain', 'event_created', 'event_published', 'event_end', 'event_start', 'fb_published', 'has_logo', 'listed', 'payee_name', 'payout_type', 'previous_payouts', 'user_created', 'user_type', 'venue_country', 'venue_latitude', 'venue_longitude']
    
    to_drop = ['previous_payouts', 'venue_latitude', 'venue_longitude'] if drop_cord else ['previous_payouts']
    
    # Put into dataframe
    data_cp = pd.DataFrame(call)
    data_cp = data_cp[keep]
    
        
    data_cp['n_previous_payouts'] = data_cp['previous_payouts'].apply(lambda x: len(x))
    
    data_cp.drop(columns=to_drop, inplace=True)
    
    data_cp['payout_type'] = data_cp['payout_type'].apply(lambda x: 1 if x=='ACH' else 2 if x=='CHECK' else 3)
    data_cp['listed'] = data_cp['listed'].apply(lambda x: 1 if x=='y' else 0)
    
    
    data_cp = create_features(data_cp)    
    data_cp = ohe_existence(data_cp, ['email_domain', 'payee_name'])
    
#      Change country, venue country, and currency
    for col in ['country', 'venue_country', 'currency']:
        method = get_country_code if re_match_fraud(col, 'country') else get_currency_code
        data_cp[col] = data_cp[col].apply(method)
#     data_cp['country'] = data_cp['country'].apply(get_country_code)
#     data_cp['venue_country'] = data_cp['venue_country'].apply(get_country_code)
#     data_cp['currency'] = data_cp['currency'].apply(get_currency_code)
    
    data_cp.fillna(-1, inplace=True)
    
    return data_cp



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
    
    
    

    