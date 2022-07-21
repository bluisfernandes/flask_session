from flask import Flask, session, request, url_for, redirect


app = Flask(__name__)
app.secret_key = b'ASJ!&EKDQ&Eihsfasa'

mc = dict()

@app.route('/')
def index():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return f"You are not logged in <a href={url_for('login')}>Login</a>"

@app.route('/login', methods=['GET', 'POST'])
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

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
