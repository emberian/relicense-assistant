
#!/usr/bin/env python3
import github3
from urllib.parse import urlparse
import sys
import os
import time

gh = github3.login(token=os.getenv("GH_API_TOKEN"))
tpl = open("single-robigalia-issue-template.txt").read()
proc = open("processed.txt", "a")

repo = sys.argv[1]

try:
    path = urlparse(repo).path[1:].strip().split("/")
    if path[1].endswith(".git"):
        path[1] = path[1][:-4]
    r = gh.repository(path[0], path[1])
    contribs = "\n".join(map(lambda u: " - [ ] @{}".format(u.login), r.iter_contributors()))
    issue_body = tpl.replace("{{project_name}}", path[1]) + "\n" + contribs
    r.create_issue("Relicense under dual MIT/Apache-2.0", body=issue_body)
    print(repo, file=proc)
    print("Done {}".format(repo))
except Exception as e:
    print("Some exception in {}".format(repo))
    print(e)
