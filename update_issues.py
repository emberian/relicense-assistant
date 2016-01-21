#!/usr/bin/env python3
import github3
from urllib.parse import urlparse
import sys
import os
import time

from license_issue import find_issue

def update(gh, repo):
    iss = find_issue(gh, repo)
    if iss is None or iss.is_closed():
        return
    for comment in iss.iter_comments():
        if "f9f99cca7ae9cc3d2e16" in comment.body:
            return
    iss.create_comment("""
My scripts have reported that they cannot open a relicensing pull request
automatically for this repository. Sorry about that! There's a simple script
here that you could use:

https://gist.github.com/kstep/f9f99cca7ae9cc3d2e16

Though be sure to change "The Rust Project Developers" to the appropriate text
in LICENSE-MIT.

Alternatively, I can create the PR manually. Either works for me, just let me
know!
""")

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
    processed = (setify("bad-pr.txt") | setify("bad-push.txt")) - setify("issue-about-bad.txt")
    ready_to_relicense = open("issue-about-bad.txt", "a")
    gh = github3.login(token=os.getenv("GH_API_TOKEN"))
    update_all(gh, processed, ready_to_relicense)
