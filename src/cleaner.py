# Import Modules
from pprint import pprint
import json
from bs4 import BeautifulSoup
from urllib.parse import urlencode
import re

import pandas as pd
import numpy as np


keep = ['country', 'currency', 'delivery_method', 'email_domain', 'event_start', 
                    'fb_published', 'listed', 'object_id', 'payee_name', 'payout_type', 
                    'previous_payouts', 'user_age', 'user_type', 'venue_country', 'venue_latitude', 
                    'venue_longitude', 'venue_name', 'venue_state']

def clean_data(data:any) -> pd.DataFrame:
    data = data[keep]
    return data


def clean_row(call:any) -> pd.Series:
    pass