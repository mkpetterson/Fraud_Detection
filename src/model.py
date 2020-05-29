# Imports
import pandas as pd
import numpy as np
import pickle

from src import cleaner

from sklearn.ensemble import  RandomForestClassifier



def make_model(df):
    """Fit and pickle model"""
    
    # Eviscerate dataset
    to_keep = ['channels', 'fb_published', 'has_logo', 'user_type', 'fraud', 'n_previous_payouts']
    model_df = df[to_keep]
    model_df = model_df.dropna()
    
    # Make model
    y = model_df.pop('fraud')
    X = model_df.copy()
    
    model = RandomForestClassifier()
    model.fit(X,y)    
    
    # Pickle model
    with open("../models/random_forest_model.pkl", 'wb') as f:
        pickle.dump(model, f)
        
    return None
    
    

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
    
    
    with open("model_name.pkl", 'w') as f:
        pickle.dump(model, f)
    
    
    # Predict on new data. Proba function returns prob of class [0,1]
    new_data = np.array(cleaner.clean_row(new_data))
    y_hat = model.predict(new_data)
    y_hat_proba = model.predict_proba(new_data.reshape(1,-1))
    
    return y_hat[0], y_hat_proba[0][1]

