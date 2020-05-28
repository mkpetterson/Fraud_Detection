# Import Modules
from pprint import pprint
import json
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import re

import pandas as pd
import numpy as np


keep = ['channels', 'country', 'currency', 'delivery_method', 'email_domain', 'event_start', 'fb_published', 'has_logo', 'listed', 'payee_name', 'payout_type', 'previous_payouts', 'user_type', 'venue_country', 'venue_latitude', 'venue_longitude']


def clean_with_target(data:any) -> pd.DataFrame:
    """ Returns clean dataframe with wanted columns """
    
    data_cp = data[keep + ['acct_type']].copy()
    data_cp['fraud'] = data_cp['acct_type'].apply(lambda x: 0 if x == 'premium' else 1)
    data_cp.drop(columns='acct_type', inplace=True)
    
    return data_cp


def clean_row(call:any) -> pd.Series:
    """ Returns clean series with wanted columns, intake taken from Client API call """
    to_keep = ['channels', 'fb_published', 'has_logo', 'user_type', 'fraud', 'n_previous_payouts']
    
    # Put into dataframe
    df = pd.DataFrame(call)
    
    
    cleaned_df = df[to_keep]
    
    return cleaned_df
    


def nuclear_option(df, new_data):
    """Takes in the cleaned dataframe and outputs a super simple df for initial model"""
    
    # Eviscerate dataset
    to_keep = ['channels', 'fb_published', 'has_logo', 'user_type', 'fraud', 'n_previous_payouts']
    model_df = df[to_keep]
    model_df = model_df.dropna()
    
    # Make model
    y = model_df.pop('fraud')
    X = model_df.copy()
    
    model = RandomForestClassifier()
    model.fit(X,y)
    
    # Predict on new data. Proba function returns prob of class [0,1]
    new_data = np.array(clean_row(new_data))
    y_hat = model.predict(new_data)
    y_hat_proba = model.predict_proba(new_data.reshape(1,-1))
    
    return y_hat, y_hat_proba[1]
    
    
    

    