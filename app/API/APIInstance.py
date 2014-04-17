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
import API.APIQueue as queue
from Analysis.ComputeEngine.ComputeEngineConfig import *
from uuid import uuid1

###########################################################################
## \brief Counts the number of active instances.
## \return returns the number of active instances.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def count():
	return instances.count()

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

###########################################################################
## \brief gets statistics about the instances.
## \return returns a tuple containing the ratio of instances to tasks, the instance count and the task count.
## \note if there are no instances but there are tasks, the ratio is infinity. If there are no instances OR tasks, the ratio is 1.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def stats():
	instance_count = count()
	task_count = queue.task_count()
	if instance_count == 0:
		if task_count == 0:
			ratio = 1
		else:
			ratio = float('inf')
	else:
		ratio = task_count / instance_count
	return (ratio, instance_count, task_count)

###########################################################################
## \brief Checks the instance to task ratio and if out of the slack ratio kills or creates instances.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def balance():
	(ratio, instance_count, task_count) = stats()
	upper_ratio_limit = CE_SCALING * (1 - CE_SLACK)
	lower_ratio_limit = CE_SCALING * (1 + CE_SLACK)

	print 'lower scale limit: ' + str(upper_ratio_limit)
	print 'upper limit: ' + str(lower_ratio_limit)

	if ratio < upper_ratio_limit and instance_count > MIN_INSTANCES:
		print 'killing'
		queue.kill()
	elif ratio > lower_ratio_limit and instance_count < MAX_INSTANCES:
		print 'starting'
		start()
	else:
		print 'doing nothing'
