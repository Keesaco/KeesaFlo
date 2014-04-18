###########################################################################
## \file app/API/APIBackground.py
## \brief Defines the API for running functions in the background (such that they don't block).
## \author rmurley@keesaco.com of Keesaco
###########################################################################
## \package app.API.APIBackground
## \brief Provides an API for running functions in the background (such that they don't block).
## \note Depends on PALBackground
## \sa app.API.PALBackground
###########################################################################

import PALBackground

###########################################################################
## \brief Runs a given function in the background.
## \param foo - function to be ran.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def run(foo):
	PALBackground.run(foo)
