from flask import Flask, session, request, url_for, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import secrets
from dotenv import load_dotenv
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

from forms import LoginForm, RegisterForm
from helpers import apology, login_required, login_admin_required, usd

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
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    group = db.Column(db.String(10), nullable=False, default='user')
    email = db.Column(db.String(40), nullable=False)

migrate = Migrate(app, db)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('username', ''):
        flash("You're already logged in", 'warning')
        return redirect(url_for('index'))
    form = LoginForm()
    print(request.form)
    if form.validate_on_submit():
        session['username'] = request.form['email']
        flash('ok', 'success')
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout/')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    print(request.form)
    print(request.method)
    print(form.validate_on_submit())
    if form.validate_on_submit():
        form_request = request.form
        new_user = User(
                username = form_request['username'] ,
                password = form_request['password'],
                email = form_request['email'],
        )
        db.session.add(new_user)
        db.session.commit()
        flash(f'Registred as {form.username.data}. Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/users/')
@login_admin_required
def users():
    return render_template('users.html',
            users=User.query.order_by(User.id).limit(20).all()
    )

@app.route('/account')
@login_required
def account():
    user = User.query.filter_by(username = session['username']).all()
    return render_template('users.html', users=user)


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
