###########################################################################
## \file app/API/APIQueue.py
## \brief Defines the task queue API for queuing tasks. Built upon PALQueue for cross-platform support.
## \author rmurley@keesaco.com of Keesaco
## \author hdoughty@keesaco.com of Keesaco
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
def gate_rectangle(	filename, coords, gatename, reverse, x_axis, y_axis):
	queue.add_task('jobs', 'gate_rec;' + filename + ';' + coords + ';' + gatename + ';' + reverse + ';' + x_axis + ';' + y_axis)

###########################################################################
## \brief Adds a task to perform a polyagonal gate on fcs data.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def gate_polygon(	filename, coords, gatename, reverse, x_axis, y_axis):
	queue.add_task('jobs', 'gate_poly;' + filename + ';' + coords + ';' + gatename + ';' + reverse + ';' + x_axis + ';' + y_axis)

###########################################################################
## \brief Adds a task to perform a circular gate on fcs data.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def gate_circle(	filename, coords, gatename, reverse, x_axis, y_axis):
	queue.add_task('jobs', 'gate_cir;' + filename + ';' + coords + ';' + gatename + ';' + reverse + ';' + x_axis + ';' + y_axis)

def gate_boolean(	filename, gatename, boolean_op, gate1_type, gate1_coords, 
	gate1_reverse, gate2_type, gate2_coords, gate2_reverse, x_axis, y_axis):
	queue.add_task('jobs', 'gate_bool;' + filename + ';'+ gate1_coords + ';' + gatename +
		';' + gate1_reverse + ';' + x_axis + ';' + y_axis + ';' + boolean_op + ';' + 
		gate1_type + ';' + gate2_type + ';' + gate2_coords + ';' + gate2_reverse)

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