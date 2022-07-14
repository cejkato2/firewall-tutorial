#!/usr/bin/python3

import sys, os, subprocess
from flask import Flask, flash, redirect, render_template, request, session, abort, json

app = Flask(__name__, static_url_path='/static')
app.secret_key = "fjdsfajfldf213"

@app.route('/')
def index_page():
    if "logged" not in session:
        session["logged"] = False
    result = ""
    if "result" in request.args and request.args["result"] == "failed":
        result = "Failed to login."

    return render_template('index.html', data={"result": result, "logged": session["logged"]})

# Serves static files
@app.route('/<path:path>')
def static_file(path):
    print(path)
    return app.send_static_file(path)

@app.route('/login/',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.form.to_dict()
        if data.get("username", "") == "admin" and data.get("password", "") == "12345":
            session["logged"] = True
            return redirect("/welcome/")

    session["logged"] = False
    #return render_template("login.html")
    return redirect("/?result=failed")

@app.route('/logout/')
def logout_page():
    session["logged"] = False
    #return render_template("login.html")
    return redirect("/")

@app.route('/welcome/')
def welcome_page():
    if "logged" not in session:
        session["logged"] = False
    if not session["logged"]:
        return redirect("/")
        
    return render_template('welcome.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

