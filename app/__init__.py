from flask import Flask, session, request, url_for, redirect, render_template, flash
from flask_bcrypt import Bcrypt
import os
import secrets
import requests
from dotenv import load_dotenv
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError


load_dotenv()

if not os.environ.get('API_URI'):
    raise RuntimeError("API_URI not set")

api_uri = os.getenv('API_URI')

# Make sure database URI is set
if not os.environ.get('DATABASE_USER_URI'):
    raise RuntimeError("DATABASE_USER_URI not set")


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', secrets.token_urlsafe())

app.config['TEMPLATES_AUTO_RELOAD'] = True

bcrypt = Bcrypt(app)

from .forms import LoginForm, RegisterForm
from .helpers import apology, login_required, login_admin_required


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id', ''):
        flash("You're already logged in", 'warning')
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = requests.get(f'{api_uri}/users', params={"email":form.email.data}).json()['users'][0]
        if user and bcrypt.check_password_hash(user['password'], form.password.data):
            session['username'] = user['username']
            session['user_id'] = user['id'] 
            return redirect(url_for('index'))
        flash('user and/or email not found', 'warning')
        return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route('/logout/')
def logout():
    # remove the username from the session if it's there
    session.clear()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = {
                'username': form.username.data ,
                'password': hashed_pw,
                'email': form.email.data,
                }
        requests.post(f'{api_uri}/user', json=new_user)
        flash(f'Registred as {form.username.data}. Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/users/')
@login_admin_required
def users():
    users = requests.get(f'{api_uri}/users').json()["users"]
    sorted_users = sorted(users, key= lambda d: d['id'])
    return render_template('users.html',
            users=sorted_users
    )

@app.route('/account')
@login_required
def account():
    user = requests.get(f'{api_uri}/users', params={"username":session['username']}).json()
    return render_template('users.html', users=user['users'])


@app.route('/routes/')
def routes():
    # Show a list of site routs
    links = [link.rule for link in app.url_map.iter_rules() if "GET" in link.methods]
    return render_template('routes.html', links=sorted(links))

@app.route('/password/', methods=['POST', 'GET'])
@login_required
def password():
    if request.method == 'POST':
        flash('Change password. TODO')
        return redirect(url_for('index'))
    else:
        return render_template('password.html')


@app.route('/userlist', methods=['GET'])
def list_users():
    users = requests.get(f'{api_uri}/users').json()
    return render_template('user_list.html',
            users=users['users']
    )


@app.route('/search/remove', methods=['POST'])
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        to_remove = list(request.form.to_dict().keys())
        if '/remove' in request.url:
            if '_method' in to_remove:
                for search_id in to_remove:
                    requests.delete(f'{api_uri}/search/{search_id}')
                return redirect(url_for('search'))
            else:
                itens = requests.get(f'{api_uri}/search').json()
                return render_template('items.html',
                    itens=itens['searchs'],
                    delete=True,
                    title='search'
                )

        elif (search := request.form.get("search")) != "":
            requests.post(f'{api_uri}/search', json={"search":search})
        return redirect(url_for('search'))

    else:
        itens = requests.get(f'{api_uri}/search').json()
        return render_template('items.html',
             itens=itens['searchs'],
             delete=False,
             title='search'
        )

@app.route('/category/remove', methods=['POST'])
@app.route('/category', methods=['GET', 'POST'])
def category():
    if request.method == 'POST':
        to_remove = list(request.form.to_dict().keys())
        if '/remove' in request.url:
            if '_method' in to_remove:
                for category_id in to_remove:
                    requests.delete(f'{api_uri}/category/{category_id}')
                return redirect(url_for('category'))
            else:
                itens = requests.get(f'{api_uri}/category').json()
                return render_template('items.html',
                    itens=itens['categories'],
                    delete=True,
                    title='category'
                )

        elif (categ := request.form.get("category")) != "":
            requests.post(f'{api_uri}/category', json={"category":categ})
        return redirect(url_for('category'))

    else:
        itens = requests.get(f'{api_uri}/category').json()
        return render_template('items.html',
             itens=itens['categories'],
             delete=False,
             title='category'
        )


def errorhandler(e):
    '''Handle error'''
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)
 

 # Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
    app.run(port=5001)
