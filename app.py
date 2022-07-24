from flask import Flask, session, request, url_for, redirect, render_template, flash
import os
import secrets
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', secrets.token_urlsafe())

@app.route('/')
def index():
    if 'username' in session:
        return f'''
                Logged in as {session["username"]} 
                <p><a href={url_for("logout")}>Logout</a></p>
                <p><a href={url_for("help")}>List of links</a></p>
                
                '''
    return f'''
            You are not logged in <a href={url_for('login')}>Login</a>
            <p><a href={url_for('help')}>List of links</a></p>
            '''

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        flash('You were successfully logged in')
        return render_template('index.html', name=session['username'])
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

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

if __name__ == "__main__":
    app.run()
