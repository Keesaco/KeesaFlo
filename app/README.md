## Django Framework Skeleton for Google App Engine

This is a skeleton implementation of the Django framework for Google App Engine.

## Run Locally
1. Download the Google App Engine Python SDK.
2. Reinstall all the depencies, as a guide all the dependencies referenced so far that need to be reinstalled are listed in the section bellow.
3. Run "dev_appserver.py" from the command line taking this directory as an argument: "dev_appserver.py Keesaco/app/appengine".
4. Local app can be viewed in browser by visting "http://localhost:8080/".
5. Local admin console can be viewed at "http://localhost:8000/".

## Dependences
So far, the dependencies to be added are:
´´´no-highlight
*app/autoload
*app/cloudstorage
*app/dbindexer
*app/djangoappengine
*app/djangotoolbox
*app/googleAPI
*app/static/css/bootstrap.css
*app/manage.py
*app/settings.py
´´´
They can be retreived from a version of the repository previous to the alpha release.

## Upload to App Engine
1. Download the Google App Engine Python SDK.
2. Run "appcfg.py update" from the command line taking this directory as an argument: "appcfg.py update Keesaco/app/appengine".

## Download from App Engine
Important: not possible if you are not the owner of the app or the uploader of the version
1. Download the Google App Engine Python SDK.
2. Run "appcfg.py download" from the command line taking a target directory as an argument: "appcfg.py download_app keesaco-spe <target_directory>". The files on the App Engine will be downloaded to <target_directory>.
