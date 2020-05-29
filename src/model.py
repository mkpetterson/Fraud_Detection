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
    

def predict_new_data(new_data):
    """Takes in the model and new data and predicts fraud"""

    with open('../models/random_forest_model.pkl', 'rb') as f:
        model = pickle.load(f)

    # Predict on new data. Proba function returns prob of class [0,1]
    new_data = np.array(cleaner.clean_row(new_data))
    y_hat = model.predict(new_data)
    y_hat_proba = model.predict_proba(new_data.reshape(1,-1))
    
    return y_hat[0], y_hat_proba[0][1]

