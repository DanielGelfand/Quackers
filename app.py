import json, sqlite3, urllib
from flask import Flask, render_template, request, session, redirect, url_for, flash
from urllib.request import urlopen
from utils import authenticate
import funcDB, time
import ssl

app = Flask(__name__)
app.secret_key = "ALRIIIIIIIIIIIIissaIIIIIIIIIIITE"

with open('data/keys.json', encoding='utf-8') as f:
    keys = json.loads(open('data/keys.json').read())
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
    '''Gets the news associated with the provided location.'''
    
    location = location.replace(" ", "%20")
    key = keys['news']
    # print(key)
    print('https://newsapi.org/v2/top-headlines?q='+location+'&apiKey=' + key)
    context = ssl._create_unverified_context()
    response = urlopen('https://newsapi.org/v2/top-headlines?q='+location+'&apiKey='+key, context=context)
    r = response.read()
    d = json.loads(r.decode('utf-8'))
    return d['articles']

def get_weather(city,state,country):
    '''Gets the weather associated with a particular location.'''
    
    city = city.replace(" ", "%20")
    state = state.replace(" ", "%20")
    country = country.replace(" ", "%20")
    if country == "US":
        country = "USA"
    key = keys['air']
    #print('http://api.airvisual.com/v2/city?city='+city+'&state='+state+'&country='+country+'&key='+key)
    response = urlopen('http://api.airvisual.com/v2/city?city='+city+'&state='+state+'&country='+country+'&key=CFqWqyRLZJMMiwDr9')
    data = response.read()
    dict = json.loads(data.decode('utf-8'))
    # print(dict)
    return dict
    #return render_template('home.html', city=dict['data']['city'],state=dict['data']['state'] ,weather = dict['data']['current']['weather'])

def get_events(postal):
    '''Gets the events associated with a particular location.'''
    
    key = keys['tm']
    #print('https://app.ticketmaster.com/discovery/v2/events.json?apikey='+key+'&postalCode='+postal)
    try:
        response = urlopen('https://app.ticketmaster.com/discovery/v2/events.json?apikey='+key+'&postalCode='+postal)
        data = response.read()
        dict = json.loads(data.decode('utf-8'))
        return dict['_embedded']['events'] #list of events
    except:
        time.sleep(2)
        response = urlopen('https://app.ticketmaster.com/discovery/v2/events.json?apikey='+key+'&postalCode=10021')
        data = response.read()
        dict = json.loads(data.decode('utf-8'))
        return dict['_embedded']['events']

def get_events_default(): #No events in the area
    '''Default events if there are none in the area'''
    
    key = keys['tm']
    response = urlopen('https://app.ticketmaster.com/discovery/v2/events.json?apikey='+key+'&postalCode=10021')
    data = response.read()
    dict = json.loads(data.decode('utf-8'))
    return dict['_embedded']['events']

@app.route('/')
def home():
    '''Renders the home page with news and weather'''
    
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
    
    # If there is an error with retrieving data from a location go to a default
    try:
        dict = get_weather(city,state,country)
        articles = get_news(city)
    except:
        dict = get_weather("New%20York",state,country)
        articles = get_news("New%20York")

    # Attach number to articles
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
    '''Handles registration page'''
    
    if request.method == "GET":
        return render_template("register.html")
    else:
        success, message = authenticate.register_user(
                request.form['username'],
                request.form['password'],
                request.form['passwordConfirmation'])
        if success:
            flash(message, "success")
            return redirect(url_for('login'))
        else:
            flash(message, "danger")
            return redirect(url_for('reg'))

@app.route('/login', methods=["GET", "POST"])
def login():
    '''Handles user login'''
    
    if request.method == "GET":
        username = authenticate.is_loggedin(session)
        if username:
            flash("You are already logged in!", "warning")
            return redirect(url_for('home'))
        else:
            return render_template("login.html")
    else:
        success, message = authenticate.login_user(
                request.form['username'],
                request.form['password'])
        if success:
            flash(message, "success")
            session['loggedin']=request.form['username']
            return redirect(url_for('dashboard', username=request.form['username']))
        else:
            flash(message, "danger")
            return redirect(url_for('login'))

@app.route('/logout', methods=["GET", "POST"])
def logout():
    '''Handles logging out of user account'''
    
    if authenticate.is_loggedin(session):
        session.pop('loggedin')
        flash("Successfully logged out.", "success")
    else:
        flash("You are not logged in!", "danger")
    return redirect(url_for('home'))

@app.route('/signUp', methods=['POST', 'GET'])
def signUp():
    '''Handles user signup'''
    
    username = request.form['username']
    password = request.form['password']
    passwordCon = request.form['passwordConfirmation']
    if funcDB.getUser(username):
        flash('username taken', "danger")
        return render_template('registration.html')
    else:
        if password == passwordCon:
            flash('registration success!', "success")
            funcDB.registerUser(username, password)
            return render_template('login.html')
        else:
            flash('passwords do not match', "danger")
            return render_template('registration.html')

@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    '''Handles user dashboard with events'''
    
    try: #if add event is submitted
        id = request.form['eventID']
        date = request.form['eventDate']
        funcDB.addEvent(session['loggedin'],id,date,"ny")
    except:
        pass
    #display events
    result = get_events(postal)
    myEvents = funcDB.getMyEvents(session['loggedin'])
    print(myEvents)
    if authenticate.is_loggedin(session):
        is_loggedin = True;
    else:
        is_loggedin = False;
        flash("You need to be logged into an account to access this page!", "danger")
        return redirect(url_for('home'))
    if result == []:
        return render_template('dashboard.html', events = result, is_loggedin = is_loggedin, noEvents = True, myEvents = myEvents)
    else:
        return render_template('dashboard.html', events = result, is_loggedin = is_loggedin, noEvents = False, myEvents = myEvents)


if __name__ == '__main__':
    app.debug = True
    app.run()
