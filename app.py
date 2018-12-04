import json, sqlite3, urllib
from flask import Flask, render_template, request, session, redirect, url_for, flash
from urllib.request import urlopen
from utils import authenticate
import funcDB

app = Flask(__name__)
app.secret_key = "ALRIIIIIIIIIIIIissaIIIIIIIIIIITE"

url = 'https://ipapi.co/json/'
r = urllib.request.urlopen(url).read()
dict = json.loads(r.decode('utf-8'))
# print(dict)
ip = dict['ip']
city = dict['city']
state = dict['region']
country = dict['country']
lat = dict['latitude']
lon = dict['longitude']
org = dict['org']
postal = dict['postal']

#print("Postal", postal)


def get_news(location):
    location = location.replace(" ", "%20")
    key = "36c5fe39553a4bd98d59ce42e54a299c"
    # print('https://newsapi.org/v2/top-headlines?q='+location+'&apiKey=' + key)
    response = urlopen('https://newsapi.org/v2/top-headlines?q='+location+'&apiKey=' + key)
    r = response.read()
    d = json.loads(r.decode('utf-8'))
    return d['articles']

def get_weather(city,state,country):
    city = city.replace(" ", "%20")
    state = state.replace(" ", "%20")
    country = country.replace(" ", "%20")
    if country == "US":
        country = "USA"
    print('http://api.airvisual.com/v2/city?city='+city+'&state='+state+'&country='+country+'&key=CFqWqyRLZJMMiwDr9')
    response = urlopen('http://api.airvisual.com/v2/city?city='+city+'&state='+state+'&country='+country+'&key=CFqWqyRLZJMMiwDr9')
    data = response.read()
    dict = json.loads(data.decode('utf-8'))
    # print(dict)
    return dict
    #return render_template('home.html', city=dict['data']['city'],state=dict['data']['state'] ,weather = dict['data']['current']['weather'])

def get_events(postal):
    response = urlopen('https://app.ticketmaster.com/discovery/v2/events.json?apikey=N6EyP6Cn4gTVMAgLHlPAOQrcibQ2HCeT&postalCode='+postal)
    data = response.read()
    dict = json.loads(data.decode('utf-8'))
    try:
        return dict['_embedded']['events'] #list of events
    except:
        return []

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

    try:
        dict = get_weather(city,state,country)
        articles = get_news(city)
    except:
        dict = get_weather("New%20York",state,country)
        articles = get_news("New%20York")

    i = 0
    for article in articles:
        article["id"] = "article" + str(i)
        i += 1

    if authenticate.is_loggedin(session):
        is_loggedin = True;
    else:
        is_loggedin = False;
    return render_template('home.html', city=dict['data']['city'],state=dict['data']['state'] ,weather = dict['data']['current']['weather'], articles=articles, is_loggedin = is_loggedin)


@app.route('/register', methods=["GET", "POST"])
def reg():
    if request.method == "GET":
        return render_template("register.html")
    else:
        success, message = authenticate.register_user(
                request.form['username'],
                request.form['password'],
                request.form['passwordConfirmation'])
        flash(message)
        if success:
            return render_template("dashboard.html")
        else:
            return redirect(url_for('reg'))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        username = authenticate.is_loggedin(session)
        if username:
            flash("You are already logged in!")
            return redirect(url_for('userpage', username=username))
        else:
            return render_template("login.html")
    else:
        success, message = authenticate.login_user(
                request.form['username'],
                request.form['password'])
        flash(message)
        if success:
            session['loggedin']=request.form['username']
            return redirect(url_for('dashboard', username=request.form['username']))
        else:
            return redirect(url_for('login'))

@app.route('/logout', methods=["GET", "POST"])
def logout():
    if authenticate.is_loggedin(session):
        session.pop('loggedin')
        flash("Successfully logged out.")
    else:
        flash("You are not logged in.")
    return redirect(url_for('home'))

@app.route('/signUp', methods=['POST', 'GET'])
def signUp():
    username = request.form['username']
    password = request.form['password']
    passwordCon = request.form['passwordConfirmation']
    if funcDB.getUser(username):
        flash('username taken')
        return render_template('registration.html')
    else:
        if password == passwordCon:
            flash('registration success')
            funcDB.registerUser(username, password)
            return render_template('login.html')
        else:
            flash('passwords do not match')
            return render_template('registration.html')

@app.route('/dashboard')
def dashboard():
    '''calendar'''
    try:
        result = get_events(postal)
    except:
        #Upper east side postal code
        result = get_events(10021)
    if authenticate.is_loggedin(session):
        is_loggedin = True;
    else:
        is_loggedin = False;
        flash("You need to be logged into an account to access this page!")
        return redirect(url_for('home'))
    return render_template('dashboard.html', events = result, is_loggedin=is_loggedin)



if __name__ == '__main__':
    app.debug = True
    app.run()
