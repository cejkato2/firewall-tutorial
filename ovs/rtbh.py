#!/usr/bin/python3

import sys, os, subprocess, re
from flask import Flask, flash, redirect, render_template, request, session, abort, json

app = Flask(__name__, static_url_path='/static')
app.secret_key = "fjdsfajfldf213"

class Flow(object):
    def __init__(self, cookie="", duration="", table="", n_packets=0, n_bytes=0, selector="", actions=""):
        self.cookie = cookie
        self.duration = duration
        self.table = table
        self.n_packets = n_packets
        self.n_bytes = n_bytes
        self.selector = selector
        self.actions = actions

    @classmethod
    def fromString(self, string):
        cookie = ""
        duration = ""
        table = 0
        n_packets = 0
        n_bytes = 0
        selector = ""
        actions = ""
        for part in string.split(", "):
            for token in part.strip().split(" "):
                if token.startswith("cookie="):
                    cookie = token.split("=")[1]
                elif token.startswith("duration="):
                    duration = token.split("=")[1]
                elif token.startswith("table="):
                    table = int(token.split("=")[1])
                elif token.startswith("n_packets="):
                    n_packets = int(token.split("=")[1])
                elif token.startswith("n_bytes="):
                    n_bytes = int(token.split("=")[1])
                elif token.startswith("actions="):
                    actions = token.split("=")[1]
                else:
                    selector = token
        return Flow(cookie, duration, table, n_packets, n_bytes, selector, actions)

    def toJSON(self):
        return {
            "cookie": self.cookie,
            "duration": self.duration,
            "table": self.table,
            "n_packets": self.n_packets,
            "n_bytes": self.n_bytes,
            "selector": self.selector,
            "actions": self.actions
        }
    def __str__(self):
        return str(vars(self))

def getFlows():
    with subprocess.Popen(["/usr/bin/ovs-ofctl", "dump-flows", "br0", "--rsort=priority"], stdout=subprocess.PIPE) as proc:
        data = proc.stdout.read()
    flows = []
    for row in data.decode("utf-8").split("\n"):
        if row:
            fl = Flow.fromString(row)
            flows.append(fl.toJSON())
    print(flows)
    return flows

def addFlow(selector, actions):
    args = ["/usr/bin/ovs-ofctl", "add-flow", "br0", f"{selector},actions={actions}"]
    print(args)
    with subprocess.Popen(args, stderr=subprocess.PIPE) as proc:
        data = proc.stderr.read()
    return data.decode("utf-8")

def removeFlow(selector):
    args = ["/usr/bin/ovs-ofctl", "del-flows", "br0", f"{selector}"]
    print(args)
    with subprocess.Popen(args, stderr=subprocess.PIPE) as proc:
        data = proc.stderr.read()
    return data.decode("utf-8")
    

@app.route('/', methods=["GET", "POST"])
def index_page():
    if request.method == "GET":
        err = session.get("err", "")
        return render_template('index.html', data={"flows": getFlows(), "err": err})
    elif request.method == "POST":
        data = request.form.to_dict()
        selector = "priority=50,ip"
        for t in ("nw_src", "nw_dst"):
            val = data.get(t, "")
            if val:
                selector += f",{t}={val}"
        actions = "drop"
        err = addFlow(selector=selector, actions=actions)
        print("Err " + err)
        session["err"] = err
        return redirect("/")

@app.route('/remove/', methods=["POST"])
def remove():
    data = request.form.to_dict()
    selector = data.get("selector", "")
    if selector:
        flows = getFlows()
        toremove = [s for s in flows if s["selector"] == selector]
        if len(toremove) == 1 and toremove[0]["actions"] == "drop":
            selector = re.sub(r"priority=[0-9]*,", "", selector) 
            err = removeFlow(selector)
        else:
            err = "Cannot delete this entry: " + selector
    else:
        err = "Cannot delete empty selector"
    session["err"] = err
    return redirect("/")



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


