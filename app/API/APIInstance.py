###########################################################################
## \file app/API/APIInstance.py
## \brief Defines the API for managing analysis instances. Built upon PALInstance for cross-platform support.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
## \package app.API.APIInstance
## \brief Provides an API for managing analysis instances.
## \note Depends on PALInstance
## \sa app.API.PALInstance
###########################################################################

import API.PALInstance as instances

###########################################################################
## \brief Counts the number of active instances.
## \return returns the number of active instances.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def count():
	instances.count()

###########################################################################
## \brief starts a new instances.
## \return returns True if successful, false otherwise.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def start():
	instances.start('f1-micro')
