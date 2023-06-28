from flask import Flask, render_template, url_for
from myapp import app

@app.route("/")
@app.route("/index")
def index_func():
    return render_template("index.html", title="Home")
    
@app.route("/register")
def register_func():
    return render_template("register.html", title="html")