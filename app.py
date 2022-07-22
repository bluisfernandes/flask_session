from flask import Flask, session, request, url_for, redirect
import os
import secrets
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', secrets.token_urlsafe())

@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]} <p><a href={url_for("logout")}>Logout</a></p>'
    return f"You are not logged in <a href={url_for('login')}>Login</a>"

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logouta/123')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/help/')
def help():
    # Show a list of site routs
    links = [link.rule for link in app.url_map.iter_rules()]
    text = '<br>'.join(links)
    return f'{text}'

if __name__ == "__main__":
    app.run()
