#Imports
from flask import Flask, request, render_template, jsonify
app = Flask(__name__)
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
#from src import pred
#from src import clean_data_func
from src import api_client
import pymongo
from pymongo import MongoClient
import mplcyberpunk 
plt.style.use("cyberpunk")
client = MongoClient('localhost', 27017)
db = client.fraud_detection

#Setup
client = api_client.EventAPIClient()

#Routes
@app.route('/', methods=['GET'])
def home():
    return ''' 
    <h1>Project Title</h1>
    <p><a href="/dashboard">dashboard</a></p>
    <p> nothing here, friend, but a link to 
                   <a href="/hello">hello</a> and an 
                   <a href="/form_example">example form</a> </p> 
                   '''

@app.route('/hello', methods=['GET'])
def hello_world():
    return ''' <h1> Hello, World!</h1> '''

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
    alpha_col = 0.7
    colors = ["g", "deeppink", "dodgerblue", "orange", "white", "purple", "red"]
    ax.bar(x, y, color=colors, alpha=alpha_col)
    mplcyberpunk.add_glow_effects()
    mplcyberpunk.add_underglow()
    fig.savefig('static/current.png')
    return render_template('dashboard.html')


@app.route('/draw', methods=['GET'])
def draw():
    one = db.fraud_detection.find()[0]
    print(one)
    return jsonify({'one': one})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)