# Import Modules
from pprint import pprint
import json
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import re

import pandas as pd
import numpy as np


keep = ['channels', 'country', 'currency', 'delivery_method', 'email_domain', 'event_start', 'fb_published', 'has_logo', 'listed', 'payee_name', 'previous_payouts', 'user_type', 'venue_country', 'venue_latitude', 'venue_longitude']


def clean_with_target(data:any) -> pd.DataFrame:
    """ Returns clean dataframe with wanted columns """
    
    data_cp = data[keep + ['acct_type']].copy()
    data_cp['fraud'] = data_cp['acct_type'].apply(lambda x: 0 if x == 'premium' else 1)
    data_cp.drop(columns='acct_type', inplace=True)
    
    return data_cp





def clean_row(call:any) -> pd.Series:
    """ Returns clean series with wanted columns, intake taken from Client API call """
    
    pass