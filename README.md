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

For convenience, an HTML copy of the documentation is accessible from keesaco.com using the following link:  
[Doxygen output](http://keesaco.com/1c314fc722274b40e8600aec4610edf1/Doxygen/html/) (Last updated 23 Feb 14)  
Please note that this may not reflect all of the latest changes to the project and only shows documentation for
code on the development branch.

Dependencies:
-------------
This project has a number of dependencies which are not committed to this repository. For convenience, the project has been prepared for automatic dependency acquisition using AppBuild.
To build the application download [AppBuild.py](http://jpm.im/AppBuild-0-0-1) and place it in the root directory of the project.
Running ‘python AppBuild.py’ will download and unzip all dependencies into their correct directories for the app to be run/deployed.

In addition to these dependencies, the application requires [pyopenssl](https://github.com/pyca/pyopenssl) to run locally. As this is not installed into the application's files it is not downloaded by AppBuild.


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
