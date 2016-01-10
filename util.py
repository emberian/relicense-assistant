from urllib.parse import urlparse

def uri_to_repo(gh, uri):
    path = urlparse(uri).path[1:].strip().split("/")
    if path[1].endswith(".git"):
        path[1] = path[1][:-4]
    return gh.repository(path[0], path[1])
