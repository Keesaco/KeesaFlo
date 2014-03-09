###########################################################################
## \file app/API/APIQueue.py
## \brief Defines the task queue API for queuing tasks. Built upon PALQueue for cross-platform support.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
## \package app.API.APIQueue
## \brief Provides an API for accessing the job queue.
## \note Depends on PALQueue
## \sa app.API.PALQueue
###########################################################################

import API.PALQueue as queue

###########################################################################
## \brief Adds a task to visualise fcs data
## \param filename - filename of fcs data to visualise
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def visualise(	filename ):
	queue.add_task('vis;' + filename)

###########################################################################
## \brief Adds a task to kill a virtual machine instance.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def kill():
    queue.add_task('kill;' + filename)