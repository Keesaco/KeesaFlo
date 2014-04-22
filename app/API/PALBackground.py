###########################################################################
## \file app/API/PALBackground.py
## \brief Contains the PALBackground package: Runs functions in the background (such that they don't block).
## \author rmurley@keesaco.com of Keesaco
###########################################################################
## \package app.API.PALBackground
## \brief Contains abstraction layer functions for the Google deferred library - returns results in a platform independent form
## \brief Provides an API for Google deferred library in a platform independant form.
###########################################################################

from google.appengine.ext import deferred

###########################################################################
## \brief Runs a given function in the background.
## \param func - function to be ran.
## \param delay - approx delay in seconds before function is run.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def run(func, delay):
	deferred.defer(func, _countdown = delay)
