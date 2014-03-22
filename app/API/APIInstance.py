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



###########################################################################
## \brief Counts the number of active instances.
## \return returns the number of active instances.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def count():
	instances.count()
