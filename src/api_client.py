"""Realtime Events API Client for DSI Fraud Detection Case Study"""
import time
import requests
import pickle
import pymongo
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('localhost', 27017)
#client = MongoClient(f"address to db/fraud_detection")
db = client.fraud_detection


#from src import pred
import cleaner
import model
    
class EventAPIClient:
    """Realtime Events API Client"""

    def __init__(self, first_sequence_number=0,
                 api_url='https://hxobin8em5.execute-api.us-west-2.amazonaws.com/api/',
                 db=None,
                 interval=30):
        """Initialize the API client."""
        self.next_sequence_number = first_sequence_number
        self.api_url = api_url
        
        with open('static/key.txt', 'r') as myfile:
            self.api_key=myfile.read().replace('\n', '')
        self.db = db
        self.interval = 30
        
#         with open('models/random_forest_model.pkl', 'rb') as myfile:
#             self.model = pickle.load(myfile)

    
#     def predict(self, row):
#         row[pred] = self.model.predict(row)
#         row[pred_proba] = self.model.predict_proba(row)
#         return row
    
    def save_to_database(self, row):
        """input cleaned data row 
           ouput: row with prediction to the database."""
        
        #add prediction columns
        #sequence_number = row.pop('sequence_number')
        
        data_dict = model.predict_new_data(row)
        time = round(datetime.timestamp(datetime.now()))
        
        # append to existing data
        
        #save cleaned data to DB
        
        db.fraud_alert.insert_one({'time': time, 'data': data_dict})
        print("Received data:\n" + repr(row) + "\n")  
        
    def get_data(self):
        """Fetch data from the API."""
        payload = {'api_key': self.api_key,
                   'sequence_number': self.next_sequence_number}
        response = requests.post(self.api_url, json=payload)
        data = response.json()
        self.next_sequence_number = data['_next_sequence_number']
        return data['data']

    def collect(self, interval=30):
        """Check for new data from the API periodically."""
        while True:
            print("Requesting data...")
            data = self.get_data()
            if data:
                print("Saving...")
                for row in data:
                    #cleaned_row = cleaner.clean_row(row)
                    #self.save_to_database(cleaned_row)
                    self.save_to_database(row)
            else:
                print("No new data received.")
            print(f"Waiting {interval} seconds...")
            time.sleep(interval)


def main():
    """Collect events every 30 seconds."""
    client = EventAPIClient()
    client.collect()


if __name__ == "__main__":
    main()
