from flask import redirect, Response
from flask import Flask
import urllib2
import json

url = "https://circleci.com/api/v1/project/kholia/JohnTheRipper?shallow=true&offset=0&limit=7"
# url = "https://circleci.com/api/v1/project/magnumripper/JohnTheRipper?shallow=true&offset=0&limit=7"
artifact_url = "/artifacts/0/home/ubuntu/builds/JtR-MinGW-%s.zip"

try:
    request = urllib2.Request(url, headers={"Accept": "application/json"})
    contents = urllib2.urlopen(request).read()
    builds = json.loads(contents)
except urllib2.URLError, e:
    print e
    raise e

for build in builds:
    build_url = build["build_url"]
    short_vcs_revision = build["vcs_revision"][:7]  # 7 is the default
    latest_build_url = build_url + (artifact_url % short_vcs_revision)
    print(latest_build_url)
