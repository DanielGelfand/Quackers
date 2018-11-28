import json, sqlite3
from flask import Flask,render_template, request, session, redirect, url_for, flash
from urllib.request import urlopen

app = Flask(__name__)
app.secret_key = "ALRIIIIIIIIIIIIissaIIIIIIIIIIITE"
@app.route('/')
def home():

    '''Weather info of location'''

    #response = urlopen('https://api.airvisual.com/v2/nearest_city?key=CFqWqyRLZJMMiwDr9')
    response = urlopen('http://api.airvisual.com/v2/city?city=New%20York&state=New%20York&country=USA&key=CFqWqyRLZJMMiwDr9')
    data = response.read()
    dict = json.loads(data.decode('utf-8'))
    print(dict)

    return render_template('home.html', city=dict['data']['city'],state=dict['data']['state'] ,weather = dict['data']['current']['weather'])


@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    '''calendar'''
    return render_template('dashboard.html')



if __name__ == '__main__':
    app.debug = True
    app.run()
