# Imports
import pandas as pd
import numpy as np
import pickle
import os

from src import cleaner

from sklearn.ensemble import  RandomForestClassifier


def make_model(df):
    """Fit and pickle model"""
    
    # Make model
    y = model_df.pop('fraud')
    X = model_df.copy()
    
    model = RandomForestClassifier()
    model.fit(X,y)    
    
    # Pickle model
    with open("../models/random_forest_model.pkl", 'wb') as f:
        pickle.dump(model, f)
        
    return None
    

def predict_new_data(new_data, model_name):
    """Takes in the model and new data and predicts fraud"""

    # Open up model
    model_name = model_name+'.pkl'
    path = os.path.join('../models/', model_name)
    print(f'Loading model from: {path}...')
    with open('../models/random_forest_modelv2.pkl', 'rb') as f:
        model = pickle.load(f)

    # Predict on new data. Proba function returns prob of class [0,1]
    try:
        new_data = cleaner.clean_row(new_data)
        np_data = np.array(new_data)
    except:
        new_data = cleaner.clean_row([new_data])
        np_data = np.array(new_data)
        
    # Make predictions    
    y_hat = model.predict(np_data)
    y_hat_proba = model.predict_proba(np_data.reshape(1,-1))
    
    # Get fraud levels
    proba_fraud, risk_level = compute_risk(y_hat_proba)
    
    # Create new df
    new_data['proba_fraud'] = proba_fraud 
    new_data['risk'] = risk_level
    
    return new_data, proba_fraud, risk_level


def compute_risk(y_hat_proba):
    
    proba_fraud = y_hat_proba[0][1]
    
    if proba_fraud < 0.1:
        risk = 'Low Risk'
    elif proba_fraud > 0.5:
        risk = 'High Risk'    
    else:
        risk = 'Medium Risk'
    
    return proba_fraud, risk
