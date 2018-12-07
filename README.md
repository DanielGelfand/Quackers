# Quackers 🦆🦆🦆

## Daniel Gelfand, Kyle Tau, Joshua Weiner, Jeffrey Wu

### Purpose
Have you **JUST** moved to a new city? Are you wondering what is going on in your city? Look no more, *QuackyInfo* is here!

Users can see plenty of information such as news headlines and weather customized to their location. Users don't even have to manually input a location as our product can find it through their IP address. Registered users also gain access to their own dashboard with upcoming events from artists in the area. How simple and useful is that? 😉

### How To Use QuackyInfo?

1. Clone the repo
    * ssh - `git@github.com:DanielGelfand/Quackers.git`
    * https - `https://github.com/DanielGelfand/Quackers.git`
2. `$ cd Quackers`
   * Move to root of repo
3. `pip install -r requirements.txt`
    * Install the requirements for QuackyInfo   
4.  `$ . location_of_venv/venv_name/bin/activate`
    * Activate your virtual environment
5. `$ python db_builder.py`
    * Initialize your database, if you have not already. This is necessary to store user accounts and saved events.
6. `$ python app.py`
    * Start QuackyInfo
7. Open up your browser and type [127.0.0.1:5000](http://127.0.0.1:5000/)
    * Load QuackyInfo in browser and enjoy

 ### How To Procure API Keys?

 * AirVisual - Create an AirVisual account and generate a key from your dashboard.
    * [Sign up here](https://www.airvisual.com/dashboard/api)
    * Copy and paste given key into the value corresponding to "air" of data/keys.json
 * News - Register to get an API key
    * [Sign up here](https://newsapi.org/register)
    * Copy and paste given key into the value corresponding to "news" of data/keys.json
 * Ticketmaster - Sign up for an account and generate a key.
    * [Sign up here](https://developer-acct.ticketmaster.com/user/register)
    * Copy and paste given key into the value corresponding to "tm" of data/keys.json
 * IPapi - No Key needed
 
 ### Dependencies - Installed by Following Use Instructions Above

* Flask
    * Flask is the framework for QuackyInfo.

* Jinja2
    * Jinja2 is a template engine for Python.

