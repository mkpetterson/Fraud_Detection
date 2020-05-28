#Imports
from flask import Flask, request
app = Flask(__name__)
#from src import pred
#from src import clean_data_func
from src import api_client

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
       



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)