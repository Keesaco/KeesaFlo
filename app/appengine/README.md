## Django Framework Skeleton for Google App Engine

This is a skeleton implementation of the Django framework for Google App Engine. Currently this only serves a static page.

## Run Locally
1. Download the Google App Engine Python SDK.
2. Run "dev_appserver.py" from the command line taking this directory as an argument: "dev_appserver.py Keesaco/app/appengine".
3. Local app can be viewed in browser by visting "http://localhost:8080/".
4. Local admin console can be viewed at "http://localhost:8000/".

## Upload to App Engine
1. Download the Google App Engine Python SDK.
2. Run "appcfg.py update" from the command line taking this directory as an argument: "appcfg.py update Keesaco/app/appengine".

## Download from App Engine
1. Download the Google App Engine Python SDK.
2. Run "appcfg.py download" from the command line taking a target directory as an argument: "appcfg.py download <target_directory>". The files on the App Engine will be downloaded to <target_directory>.