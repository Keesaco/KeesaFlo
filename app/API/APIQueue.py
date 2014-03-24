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
	queue.add_task('jobs', 'vis;' + filename)

###########################################################################
## \brief Adds a task to kill a virtual machine instance.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def kill():
	queue.add_task('jobs', 'kill')

###########################################################################
## \brief Adds a task to perform a rectangle gate on fcs data.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def gate_rectangle(	filename, coords, gatename):
	queue.add_task('jobs', 'gate_rec;' + filename + ';' + coords + ';' + gatename)

###########################################################################
## \brief Adds a task to perform a polyagonal gate on fcs data.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def gate_polygon(	filename, coords, gatename):
	queue.add_task('jobs', 'gate_poly;' + filename + ';' + coords + ';' + gatename)

###########################################################################
## \brief Adds a task to perform a circular gate on fcs data.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def gate_circle(	filename, coords, gatename):
	queue.add_task('jobs', 'gate_cir;' + filename + ';' + coords + ';' + gatename)

###########################################################################
## \brief Adds a task to perform a circular gate on fcs data.
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
def change_axis(	filename, x_axis, y_axis):
	queue.add_task('jobs', 'change_axis;' + filename + ';' + x_axis + ';' + y_axis)

###########################################################################
## \brief Counts the number of tasks in the queue.
## \return number of tasks in queue.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def task_count():
	return queue.task_count('jobs')