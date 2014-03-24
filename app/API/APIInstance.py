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
from Analysis.ComputeEngine.ComputeEngineConfig import *
from uuid import uuid1

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
	## Generate unique identifier, removing hyphens.
	id = UNIQUE_NAME + '-' + str(uuid1())
	## Create persistent disk.
	print instances.create_disk(id)
	## Start instance.
	print instances.start(id, id)
