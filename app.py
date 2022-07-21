from flask import Flask


app = Flask(__name__)

mc = dict()

@app.route("/")
def home():
    mc.update({"foo": "barra"})
    return mc.get("foo", 'não tem')

@app.route("/q")
def q():
    mc.update({"foo": "barra Q"})
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
