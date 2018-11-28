import json, sqlite3
from flask import Flask, render_template, request, session, redirect, url_for, flash
from urllib.request import urlopen

app = Flask(__name__)
app.secret_key = "ALRIIIIIIIIIIIIissaIIIIIIIIIIITE"

url = 'https://ipapi.co/json/'
r = urllib.request.urlopen(url).read()
dict = json.loads(r)
print(dict)
ip = dict['ip']
city = dict['city']
state = dict['region']
country = dict['country']
lat = dict['latitude']
lon = dict['longitude']
org = dict['org']




def get_news(location):
    key = "36c5fe39553a4bd98d59ce42e54a299c"
    response = urlopen('https://newsapi.org/v2/top-headlines?keyword='+location+'&apiKey=' + key)
    r = response.read()
    d = json.loads(r.decode('utf-8'))
    return d['articles']


def get_weather(city,state,country):

    response = urlopen('http://api.airvisual.com/v2/city?city={}&state={}&country={}&key=CFqWqyRLZJMMiwDr9'.format(city,state,country))
    data = response.read()
    dict = json.loads(data.decode('utf-8'))
    #print(dict)
    return dict
    #return render_template('home.html', city=dict['data']['city'],state=dict['data']['state'] ,weather = dict['data']['current']['weather'])



@app.route('/')
def home():
    '''url = 'https://ipapi.co/json/'
    r = urllib.request.urlopen(url).read()
    dict = json.loads(r)
    print(dict)
    ip = dict['ip']
    region = dict['region']
    country = dict['country']
    lat = dict['latitude']
    lon = dict['longitude']
    org = dict['org']'''
    '''Weather info of location'''

    #response = urlopen('https://api.airvisual.com/v2/nearest_city?key=CFqWqyRLZJMMiwDr9')
    '''response = urlopen('http://api.airvisual.com/v2/city?city=New%20York&state=New%20York&country=USA&key=CFqWqyRLZJMMiwDr9')
    data = response.read()
    dict = json.loads(data.decode('utf-8'))
    print(dict)'''

    get_weather(city,state,country)
    articles = get_news("New York")

    return render_template('home.html', city=dict['data']['city'],state=dict['data']['state'] ,weather = dict['data']['current']['weather'], articles=articles)


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
