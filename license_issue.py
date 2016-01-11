#!/usr/bin/env python3
import github3
from urllib.parse import urlparse
import sys
import os
import time

from util import uri_to_repo

def find_issue(gh, repo):
    r = uri_to_repo(gh, repo)
    for issue in r.iter_issues(since="2016-01-07T00:00:00Z"):
        if issue.title == "Relicense under dual MIT/Apache-2.0":
            return issue

if __name__ == "__main__":
    gh = github3.login(token=os.getenv("GH_API_TOKEN"))
    if gh is None:
        print("Could not authenticate to GitHub", file=sys.stderr)
        sys.exit(1)
    iss = find_issue(gh, sys.argv[1])
    if iss is None:
        print("No relicensing issue found", file=sys.stderr)
        sys.exit(1)
    print(iss.html_url)
    if iss.is_closed():
        sys.exit(2)
