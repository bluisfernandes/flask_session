import bmemcached
import os
from flask import Flask


app = Flask(__name__)

servers = os.environ.get('MEMCACHIER_SERVERS', '').split(',')
user = os.environ.get('MEMCACHIER_USERNAME', '')
passw = os.environ.get('MEMCACHIER_PASSWORD', '')

mc = bmemcached.Client(servers, username=user, password=passw)

mc.enable_retry_delay(True)  # Enabled by default. Sets retry delay to 5s.

@app.route("/")
def home():
    mc.set("foo", "barra")
    return mc.get("foo", 'não tem')

@app.route("/q")
def q():
    mc.set("foo", "barra Q")
    return mc.get("foo", 'não tem Q')

@app.route("/qq")
def qq():
    resp = mc.get("foo", 'não tem QQ1')
    return f'/ qq \t{resp}'

@app.route("/qqq")
def qq2():
    resp = mc.get("foo", 'não tem QQ2')
    return f'/ qqq \t{resp}'

if __name__ == "__main__":
    app.run()
