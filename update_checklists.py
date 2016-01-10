#!/usr/bin/env python3
import github3
from urllib.parse import urlparse
import sys
import os
import time

from util import uri_to_repo

considered_agreed = [
        "i consent",
        "i license past and future contributions under the dual mit/apache-2.0 license, allowing licensees to chose either at their option",
        "r+",
        "i agree",
        ]


def update(gh, repo):
    r = uri_to_repo(gh, repo)
    iss = None
    for issue in r.iter_issues(since="2016-01-07T00:00:00Z"):
        if issue.title == "Relicense under dual MIT/Apache-2.0":
            iss = issue
    if iss is None or iss.is_closed():
        return
    agreed = []
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
        except e:
            print("Exception in {}".format(uri))
            print(e)

if __name__ == "__main__":
    processed = set(map(str.strip, set(open("processed.txt")))) - set(map(str.strip, set(open("ready.txt"))))
    ready_to_relicense = open("ready.txt", "a")
    gh = github3.login(token=os.getenv("GH_API_TOKEN"))
    update_all(gh, processed, ready_to_relicense)
