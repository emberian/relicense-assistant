#!/usr/bin/env python3
import github3
from urllib.parse import urlparse
import sys
import os
import time

from license_issue import find_issue

considered_agreed = [
        "i license past and future contributions under the dual mit/apache-2.0 license, allowing licensees to chose either at their option",
        "r+",
        ]


def update(gh, repo):
    iss = find_issue(gh, repo)
    if iss is None or iss.is_closed():
        return
    agreed = ["cmr", "homu", "gitter-badger"]
    for comment in iss.iter_comments():
        if any(text in comment.body.lower() for text in considered_agreed):
            agreed.append(comment.user.login)
    new_text = iss.body
    for u in agreed:
        print("{} agreed".format(u))
        new_text = new_text.replace("[ ] @{}".format(u), "[x] @{}".format(u))
    iss.edit(body=new_text)
    if "[ ]" in new_text:
        return False
    return True

def update_all(gh, processed, ready_to_relicense):
    for uri in processed:
        try:
            if update(gh, uri):
                print(uri, file=ready_to_relicense)
            print("{} updated!".format(uri))
        except Exception as e:
            print("Exception in {}".format(uri))
            print(e)
        time.sleep(2)

def setify(fname):
    return set(map(str.strip, set(open(fname))))

if __name__ == "__main__":
    processed = setify("processed.txt") - setify("ready.txt") - setify("no-issue.txt")
    ready_to_relicense = open("ready.txt", "a")
    gh = github3.login(token=os.getenv("GH_API_TOKEN"))
    update_all(gh, processed, ready_to_relicense)
