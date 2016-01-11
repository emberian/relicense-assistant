import sys
from urllib.parse import urlparse

def uri_to_repo(uri):
    path = urlparse(uri).path[1:].strip().split("/")
    if path[1].endswith(".git"):
        path[1] = path[1][:-4]
    return path[1]

if __name__ == "__main__":
    print(uri_to_repo(sys.argv[1]))
