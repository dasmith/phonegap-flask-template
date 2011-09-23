"""
BEST FRIEND FIRST SEARCH 

Python Requirements:
    - flask
    - flaskext-login
    - sqlite3

2011-09-23 

Dustin Smith
Kasia Hayden
"""
import os
from functools import wraps

import sqlite3
from flask import *
from contextlib import closing

DATABASE = os.getcwd()+'/../db/database.db'
GOOGLE_API_KEY = "anothersecret"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bestkeptsecret'

## SQLite Helper Functions
## From http://flask.pocoo.org/docs/patterns/sqlite3/
def connect_db():
    return sqlite3.connect(DATABASE)

def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

# Doesn't exist until Flask 8
#@app.before_first_request
#def before_first_request():
#    g.user = None
     
@app.before_request
def before_request():
    print "Before request"
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

def login_required(f):
    """
    Simple login decorator from
    http://flask.pocoo.org/docs/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'user' in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def check_user_login(email, password):
    """
    Looks up a user in the SQLite Db
    """
    user = query_db('select * from tbl_users where email = ? and password = ?',
                    [email, password], one=True)
    if user is None:
        print 'No such user'
    else:
        print email, 'has the id', user['id']
    return user
    

## Controllers for webpages
@app.route("/logout/")
#@login_required
def logout():
  flash("You have been logged out")
  return redirect("/login")



##################################################################################
#  User session management and Stay monitoring controllers 
##################################################################################

@app.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = check_user_login(email=email, password=password)
        if user == None:
            flash("Terrible login credentials.")
            return redirect(url_for("index")) 
        session['user'] = user
        print "Set user to", user
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("_login.html")

@app.route("/")
@login_required
def index():
  return render_template("main.html", 
                         user=session['user'],
                         google_api_key=GOOGLE_API_KEY)
                         
                         
def init_db():
    print "Initializing Database...."
    with closing(connect_db()) as db:
        with app.open_resource('../db/schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


# if database doesn't exist, initialize it
try:
   open(DATABASE)
except IOError as e:
   init_db()

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=6060)

