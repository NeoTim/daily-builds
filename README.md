# HOWTO

* Download [Google App Engine Python SDK](https://cloud.google.com/appengine/docs/standard/python/download).

* Setup application libraries,

  ```
  $ pip install -t lib -r requirements.txt
  ```

* Test the application using `dev_appserver.py`.

  ```
  $ ~/google-cloud-sdk/bin/dev_appserver.py app.yaml
  ```

* Use the following commands for deploying the application.

  ```
  $ ~/google-cloud-sdk/bin/gcloud app deploy app.yaml --project daily-builds

  ```

* Check application logs by running the following command,

  ```
  $ ~/google-cloud-sdk/bin/gcloud app logs read -s default
  ```


# App Engine Standard Flask Hello World

This sample shows how to use [Flask](http://flask.pocoo.org/) with Google App
Engine Standard.

Before running or deploying this application, install the dependencies using
[pip](http://pip.readthedocs.io/en/stable/):

    pip install -t lib -r requirements.txt

For more information, see the [App Engine Standard README](../../README.md)
