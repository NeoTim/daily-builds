from flask import redirect, Response
from flask import Flask
import urllib2
import json
from google.appengine.api import urlfetch

app = Flask(__name__)
app.config['DEBUG'] = True


# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

@app.route('/')
def hello():
    return 'Hello World v4!'


@app.route('/latest')
def latest():
    url = "https://circleci.com/api/v1/project/magnumripper/JohnTheRipper?shallow=true&offset=0&limit=7"
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
        # does this build even exist?
        """
        request = urllib2.Request(latest_build_url)
        request.get_method = lambda: 'HEAD'
        try:
            urllib2.urlopen(request)
        except urllib2.HTTPError as e:
            if e.code == 404:
                continue
        """
        try:
            result = urlfetch.fetch(latest_build_url, follow_redirects=True, method="HEAD")
            if result.status_code == 200:
                return redirect(latest_build_url)
            else:
                print result.status_code, "Problem while querying latest_build_url!"
                continue
        except urlfetch.Error:
            print 'Caught exception fetching url!'
            continue


@app.route('/builds')
def builds():
    url = "https://circleci.com/api/v1/project/magnumripper/JohnTheRipper?shallow=true&offset=0&limit=7"

    try:
        request = urllib2.Request(url, headers={"Accept": "application/json"})
        contents = urllib2.urlopen(request).read()
        return Response(response=contents,
                        status=200,
                        mimetype="application/json")
    except urllib2.URLError, e:
        print e


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404


@app.route('/latest_inactive')
def latest_inactive():
    url = "https://api.github.com/repos/magnumripper/JohnTheRipper/commits"

    try:
        request = urllib2.Request(url, headers={"Accept": "application/json"})
        content = urllib2.urlopen(request).read()
        commits = json.loads(content)
        for commit in commits:
            short_vcs_revision = commit["sha"][:7]  # 7 is the default
            latest_build_url = "http://45.33.2.252:2443/JtR-sse2-%s.zip" % short_vcs_revision  # Jim's machine
            # does this build even exist?
            request = urllib2.Request(latest_build_url)
            request.get_method = lambda: 'HEAD'
            try:
                urllib2.urlopen(request)
            except urllib2.HTTPError as e:
                if e.code == 404:
                    continue
            return redirect(latest_build_url)
    except urllib2.URLError, e:
        print e

    return 'Hello World!'
