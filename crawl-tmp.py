#!/usr/bin/env python3
import github3
import requests
import json
import os
import sys

index = os.getenv("CRATES_INDEX")

def handle_crate(name):
    crate = requests.get("https://crates.io/api/v1/crates/{}".format(name))
    j = crate.json()
    if "errors" in j:
        return
    j = j["crate"]
    if "license" in j:
        if j["license"] is None:
            return
        if j["license"] == "Apache-2.0":
            print("ok")
        print("nope", file=sys.stderr)
        return

for dname, subdirs, files in os.walk(index):
    for fname in files:
        handle_crate(fname)
