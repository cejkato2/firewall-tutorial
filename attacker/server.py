#!/usr/bin/python3

import sys, os, subprocess
from flask import Flask, flash, redirect, render_template, request, session, abort, json

app = Flask(__name__)

class Attack(object):
    @classmethod
    def getName(self):
        return "Attack"
    def getStatus(self):
        return False
    def getResult(self):
        return ""
    def start(self):
        pass
    def stop(self):
        pass
    def getJSON(self):
        return {"name": self.getName(),
        "status": self.getStatus(),
        "result": self.getResult()}

class AttackBruteForce(Attack):
    @classmethod
    def getName(self):
        return "BruteForce"

    def getStatus(self):
        rv = os.system("pgrep bf.py > /dev/null")
        return rv == 0

    def getResult(self):
        try:
            with open("/tmp/pwned", "r") as f:
                content = f.read()
            return content
        except Exception:
            return ""

    def start(self):
        if not self.getStatus():
            #os.spawnl(os.P_NOWAIT, "")
            pid = subprocess.Popen(["nohup /vagrant/bf.py 172.16.10.2:8080 >> /var/log/bf.out 2>> /var/log/bf.err&"], shell=True, close_fds=True).pid
            print(f"running bf.py with pid {pid}")
            #subprocess.Popen(["/vagrant/bf.py"], shell=True, close_fds=True)
    def stop(self):
        os.system("pkill -9 bf.py")

class AttackDDoS(Attack):
    @classmethod
    def getName(self):
        return "DDoS"

    def getStatus(self):
        rv = os.system("pgrep ddos.py > /dev/null")
        return rv == 0

    def start(self):
        if not self.getStatus():
            #os.spawnl(os.P_NOWAIT, "")
            pid = subprocess.Popen(["nohup /vagrant/ddos.py 172.16.10.2 >> /var/log/ddos.out 2>> /var/log/ddos.err&"], shell=True, close_fds=True).pid
            print(f"running ddos.py with pid {pid}")
            #subprocess.Popen(["/vagrant/bf.py"], shell=True, close_fds=True)
    def stop(self):
        os.system("pkill -9 ddos.py")

attacks = {
    AttackBruteForce.getName(): AttackBruteForce(),
    AttackDDoS.getName(): AttackDDoS(),
    }

def getData():
    global attacks
    return [attacks[a].getJSON() for a in attacks]

@app.route('/status.json')
def status():
    response = app.response_class(
        response=json.dumps(getData()),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/')
def index_page():
    return render_template('index.html', attacks=getData())

@app.route('/trig-attack/<string:name>')
def trigger_attack(name):
    global attacks
    att = attacks[name]
    if att.getStatus():
        print("Stopping...")
        att.stop()
    else:
        print("Starting...")
        att.start()
    return redirect("/")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

