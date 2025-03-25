from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Testna začetna stran deluje!</h1>"

@app.route('/home')
def home():
    return "<h1>Deluje – to je direktni response brez predloge!</h1>"

@app.route('/admin')
def admin():
    return "<h1>Admin testna stran deluje!</h1>"
