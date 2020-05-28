# Imports
import pandas as pd
import numpy as np

from sklearn.ensemble import  RandomForestClassifier





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