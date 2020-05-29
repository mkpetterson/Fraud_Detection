#Imports
from flask import Flask, request
app = Flask(__name__)

from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

#from src import pred
#from src import clean_data_func

from src import api_client

import pymongo
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.fraud_detection

#Setup
client = api_client.EventAPIClient()

#Routes
@app.route('/', methods=['GET'])
def home():
    return ''' 
    <h1>Fraud Detection</h1>
    <p>check out our dashboard:
        <a href="/dashboard">dashboard</a>
    </p>
    <p> tell us more about yourself
        <a href="/form_example">example form</a> 
    </p> 
                   '''

# @app.route('/hello', methods=['GET'])
# def hello_world():
#     return ''' <h1> Hello, World!</h1> '''

@app.route('/form_example', methods=['GET'])
def form_display():
    return ''' <form action="/string_reverse" method="POST">
                <input type="text" name="some_string" />
                <input type="submit" />
               </form>
             '''

@app.route('/string_reverse', methods=['POST'])
def reverse_string():
    text = str(request.form['some_string'])
    reversed_string = text[-1::-1]
    return ''' output: {}  '''.format(reversed_string)



@app.route('/dashboard', methods=['GET'])
def display_dash():
    data = db.fraud_detection.find()
    
    count = Counter()
    for i in data:
        count[i['data']['country']] += 1
    fig, ax = plt.subplots()
    x = np.arange(len(count.keys()))
    y = count.values()
    ax.bar(x, y)
    fig.savefig('static/current.png')
    return '''
     <h1>Fraud Dashboard</h1>
     
    <img src='static/current.png'>
    
    '''



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)