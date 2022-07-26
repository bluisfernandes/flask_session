from flask import Flask, session, request, url_for, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import secrets
from dotenv import load_dotenv
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

from helpers import apology, login_required, lookup, usd

load_dotenv()


# Make sure database URI is set
if not os.environ.get('DATABASE_USER_URI'):
    raise RuntimeError("DATABASE_USER_URI not set")


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', secrets.token_urlsafe())
 # Custom filter
app.jinja_env.filters["usd"] = usd

app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_USER_URI')

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    group = db.Column(db.String(80), nullable=True)

app.db = db.init_app(app)
Migrate(app, db)


@app.route('/')
def index():
    if session.get('username', ''):
        return render_template("index.html")
    else:
        return render_template("index.html")


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        flash('You were successfully logged in')
        # return render_template('index.html', name=session['username'])
        return render_template("index.html")
    return render_template('login.html')

@app.route('/logout/')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form = request.form
        new_user = User(
                username = form['username'] ,
                password = form['password'],
                group = form['group']
        )
        db.session.add(new_user)
        db.session.commit()

        flash("Registered")
        return redirect(url_for('table'))
    else:
        if session:
            flash("You're already registred")
            return redirect(url_for('index'))
        else:
            return render_template('register.html')

@app.route('/users/')
def table():
    return render_template('users.html',
            users=User.query.order_by(User.id).limit(20).all()
    )


@app.route('/routes/')
def routes():
    # Show a list of site routs
    links = [link.rule for link in app.url_map.iter_rules()]
    return render_template('routes.html', links=sorted(links))

@app.route('/password/', methods=['POST', 'GET'])
@login_required
def password():
    if request.method == 'POST':
        flash('Change password. TODO')
        return redirect(url_for('index'))
    else:
        return render_template('password.html')


def errorhandler(e):
    '''Handle error'''
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)
 

 # Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
    app.run()
