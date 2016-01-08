#!/usr/bin/env python3
import github3
import requests
import json
import os
import sys

index = os.getenv("CRATES_INDEX")
log_file = open("repos.txt", "w")
no_repo = open("no_repos.txt", "w")
unlic = open("unlic.txt", "w")

def handle_crate(name):
    crate = requests.get("https://crates.io/api/v1/crates/{}".format(name))
    j = crate.json()
    if "errors" in j:
        return
    j = j["crate"]
    if "license" in j:
        if j["license"] is None:
            print(name, file=unlic)
            return
        mit = "MIT" in j["license"]
        apache = "Apache-2.0" in j["license"]
        print("{} license: {}, {}, {}".format(name, mit, apache, j["license"]))
        if mit ^ apache:
            if "repository" in j and j["repository"] is not None and "github.com" in j["repository"]:
                print("{} needs to be handled".format(name))
                print(j["repository"], file=log_file)
            else:
                print(name, file=no_repo)
    else:
        print(name, file=unlic)

for dname, subdirs, files in os.walk(index):
    for fname in files:
        handle_crate(fname)
