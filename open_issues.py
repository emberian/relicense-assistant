#!/usr/bin/env python3
import github3
from urllib.parse import urlparse
import sys
import os
import time

gh = github3.login(token=os.getenv("GH_API_TOKEN"))
tpl = open("issue-template.txt").read()

repos = set(open("repos.txt"))
processed = set(open("processed.txt")).union(set(open("errored.txt")))
p = open("processed.txt", "a")
errored = open("errored.txt", "a")
ignore_users = set(open("ignores.txt"))
for repo in repos - processed:
    if any(a.strip() in repo for a in ignore_users):
        continue
    try:
        path = urlparse(repo).path[1:].strip().split("/")
        if path[1].endswith(".git"):
            path[1] = path[1][:-4]
        r = gh.repository(path[0], path[1])
        contribs = "\n".join(map(lambda u: " - [ ] @{}".format(u.login), r.iter_contributors()))
        if "@cgaebel" in contribs:
            break
        issue_body = tpl.replace("{{project_name}}", path[1]) + "\n" + contribs
        r.create_issue("Relicense under dual MIT/Apache-2.0", body=issue_body)
        print(repo.strip(), file=p)
        print("Done {}".format(repo))
        time.sleep(10)
    except Exception as e:
        print("Some exception in {}".format(repo))
        print(e)
        print(repo, file=errored)
