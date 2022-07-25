from flask import Flask, session, request, url_for, redirect, render_template, flash
import os
import secrets
from dotenv import load_dotenv
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError

from helpers import apology, login_required, lookup, usd

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', secrets.token_urlsafe())
 # Custom filter
app.jinja_env.filters["usd"] = usd


@app.route('/')
def index():
    if 'username' in session:
        return render_template("index.html")

    return f'''
            You are not logged in <a href={url_for('login')}>Login</a>
            <p><a href={url_for('help')}>List of links</a></p>
            '''

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


@app.route('/escape')
def try_escape():
    return ''' 
          /escape/some_value <br>
          /noescape/same_value <br>
            <br>
          script alert("bad") /script
            '''

@app.route('/noescape/<value>')
def no_escape(value):
    return f'Hello, {value}'


@app.route('/escape/<value>')
def with_escape(value):
    return f'Hello, {value}'

@app.route('/template/')
def template():
    return render_template('index.html', name='name_here')

@app.route('/help/')
def help():
    # Show a list of site routs
    links = [link.rule for link in app.url_map.iter_rules()]
    text = '<br>'.join(links)
    return f'{text}'

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
