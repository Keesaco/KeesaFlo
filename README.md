SPE
===
Software Product Engineering - Flow Cytometry Project

Discussion:
-----------
For discussions see the [Keesaco mailing list](https://groups.google.com/forum/#!forum/keesaco). (For access [contact Jack McCrea](mailto:jmccrea@keesaco.com))  
Issues should be raised on the repository's [issue list](https://github.com/JackMcCrea/Keesaco/issues).

Documentation:
---------------
This project is prepared for [Doxygen](http://www.doxygen.org/) automatic documentation generation.
Running Doxygen on Doxyfile.doxyfile (in the root directory of the repository) will generate documentation
for the project into the Doxygen directory in HTML and LaTeX.  
JavaScript documentation is performed automatically using js2doxy (acquired by AppBuild - see dependencies), therefore perl is required to generate documentation for JavaScript.

For convenience, an HTML copy of the documentation is accessible from keesaco.com using the following link:  
[Doxygen output](http://keesaco.com/1c314fc722274b40e8600aec4610edf1/Doxygen/html/) (Last updated 25 Mar 14)  
Please note that this may not reflect all of the latest changes to the project and only shows documentation for
code on the development branch.

Dependencies:
-------------
This project has a number of dependencies which are not committed to this repository. For convenience, the project has been prepared for automatic dependency acquisition using AppBuild.
To build the application download [AppBuild.py](http://jpm.im/AppBuild-0-0-1) and place it in the root directory of the project.
Running ‘python AppBuild.py’ will download and unzip all dependencies into their correct directories for the app to be run/deployed.

In addition to these dependencies, the application requires [pyopenssl](https://github.com/pyca/pyopenssl) to run locally. As this is not installed into the application's files it is not downloaded by AppBuild.

Testing:
--------
Automated unit testing is included in this project. Given that functionality largely relies on the Google Cloud Platform, these tests must be run using the dev_appserver. When the app is being served by the dev server, navigate to http://localhost:8080/_ah/unittest/ (changing the port if necessary).
New tests can be added by adding additional methods to existing Python files in the app/test directory, or by adding new test files to the app/test directory and then importing them from app/test/__init__.py.

Running with Local Dev Server:
------------------------------
1. Download the [Google App Engine Python SDK](https://developers.google.com/appengine/downloads).
2. Acquire dependencies using AppBuild as described above.
3. Add an (existing) application to the dev_appserver using the 'app' directory as the path.

Contact:
--------
**All members** - info@keesaco.com

Contributors:
 * Jack McCrea - jmccrea@keesaco.com  
 * Sam Whitehouse - swhitehouse@keesaco.com  
 * Christian Wike - cwike@keesaco.com  
 * Rogan Murley - rmurley@keesaco.com  
 * Matthieu Rudelle - mrudelle@keesaco.com  
 * Hazel Doughty - hdoughty@keesaco.com  
