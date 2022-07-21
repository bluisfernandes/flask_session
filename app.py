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
    mc.set("foo", "bar")
    return mc.get("foo", 'não tem')

@app.route("/q")
def q():
    mc.set("foo", "bar")
    return mc.get("foo", 'não tem Q')

if __name__ == "__main__":
    app.run()
