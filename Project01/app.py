import json, sqlite3, urllib
from flask import Flask, render_template, request, session, redirect, url_for, flash
from urllib.request import urlopen
from util import authenticate

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




def get_news(location):
    location = location.replace(" ", "%20")
    key = "36c5fe39553a4bd98d59ce42e54a299c"
    print('https://newsapi.org/v2/top-headlines?q='+location+'&apiKey=' + key)
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
    # print('http://api.airvisual.com/v2/city?city='+city+'&state='+state+'&country='+country+'&key=CFqWqyRLZJMMiwDr9')
    response = urlopen('http://api.airvisual.com/v2/city?city='+city+'&state='+state+'&country='+country+'&key=CFqWqyRLZJMMiwDr9')
    data = response.read()
    dict = json.loads(data.decode('utf-8'))
    # print(dict)
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

    dict = get_weather(city,state,country)
    articles = get_news(city)
    i = 0
    for article in articles:
        article["id"] = "article" + str(i)
        i += 1

    return render_template('home.html', city=dict['data']['city'],state=dict['data']['state'] ,weather = dict['data']['current']['weather'], articles=articles)

@app.route('/dashboard')
def dashboard():
    '''calendar'''
    return render_template('dashboard.html')

app.route('/register', methods=["GET", "POST"])
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
            return redirect(url_for('login'))
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
            return redirect(url_for('home')
        else:
            return redirect(url_for('login'))

if __name__ == '__main__':
    app.debug = True
    app.run()
