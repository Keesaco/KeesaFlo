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
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
def gate_rectangle(	filename, coords, gatename, reverse, x_axis, y_axis):
	queue.add_task('jobs', 'gate_rec;' + filename + ';' + coords + ';' + gatename + ';' + reverse + ';' + x_axis + ';' + y_axis)

###########################################################################
## \brief Adds a task to perform a polyagonal gate on fcs data.
## \author rmurley@keesaco.com of Keesaco
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
def gate_polygon(	filename, coords, gatename, reverse, x_axis, y_axis):
	queue.add_task('jobs', 'gate_poly;' + filename + ';' + coords + ';' + gatename + ';' + reverse + ';' + x_axis + ';' + y_axis)

###########################################################################
## \brief Adds a task to perform a circular gate on fcs data.
## \author rmurley@keesaco.com of Keesaco
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
def gate_circle(	filename, coords, gatename, reverse, x_axis, y_axis):
	queue.add_task('jobs', 'gate_cir;' + filename + ';' + coords + ';' + gatename + ';' + reverse + ';' + x_axis + ';' + y_axis)

###########################################################################
## \brief Adds a task to perform a boolean gate on fcs data.
## \param filename - name of fcs file to gate
## \param gatename - name of gate to be created
## \param boolean_op - boolean operator to be used to join the two gates: 'and' or 'or'
## \param gate1_type - type of first gate to be created: 'rect', 'oval' or 'poly'
## \param gate1_coords - string of all the points which define the first gate
## \param gate1_reverse - boolean representing whether cells in gate 1 are kept or removed
## \param gate2_type - type of second gate to be created
## \param gate2_coords - string of all the points which define the second gate
## \param gate2_reverse - boolean representing whether cells in gate 2 are kept or removed
## \param x_axis - name of x_axis desired for first gate, also used for visualisation
## \param y_axis - name of y_axis desired for first gate, also used for visualisation
## \param gate2_x_axis - name of x_axis desired for second gate
## \param gate2_y_axis - name of y_axis desired for second gate
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
def gate_boolean(	filename, gatename, boolean_op, gate1_type, gate1_coords, 
	gate1_reverse, gate2_type, gate2_coords, gate2_reverse, x_axis, y_axis, gate2_x_axis, gate2_y_axis):
	queue.add_task('jobs', 'gate_bool;' + filename + ';'+ gate1_coords + ';' + gatename +
		';' + gate1_reverse + ';' + x_axis + ';' + y_axis + ';' + boolean_op + ';' + 
		gate1_type + ';' + gate2_type + ';' + gate2_coords + ';' + gate2_reverse + ';' +
		gate2_x_axis + ';' + gate2_y_axis)

###########################################################################
## \brief Adds a task to perform a gate based on a bivariate normal distribution.
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
def gate_normal(	filename, gatename, reverse, x_axis, y_axis, scale_factor):
	queue.add_task('jobs', 'gate_norm;' + filename + ';' + gatename + ';' + reverse + ';' + 
		x_axis + ';' + y_axis + ';' + scale_factor)

###########################################################################
## \brief Adds a task to split data up into four quadrants based on x and y coordinate.
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
def gate_quadrant(	filename, xcoord, ycoord, quadrant1name, quadrant2name, 
	quadrant3name, quadrant4name, x_axis, y_axis):
	queue.add_task('jobs', 'gate_quad;' + filename + ';' + xcoord + ';' + ycoord + ';' + 
		quadrant1name + ';' + quadrant2name + ';' + quadrant3name + ';' + quadrant4name + 
		';' + x_axis + ';' + y_axis)

###########################################################################
## \brief Adds a task to perform a circular gate on fcs data.
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
def change_axis(	filename, x_axis, y_axis):
	queue.add_task('jobs', 'change_axis;' + filename + ';' + x_axis + ';' + y_axis)

###########################################################################
## \brief Adds a task to create a dot plot of fcs data.
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
def dot_plot(	filename, plot_name, x_axis, y_axis):
	queue.add_task('jobs', 'dot_plot;' + filename + ';' + x_axis + ';' + y_axis + ';' + plot_name)

###########################################################################
## \brief Adds a task to create a contour plot of fcs data.
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
def contour_plot(	filename, plot_name, x_axis, y_axis):
	queue.add_task('jobs', 'contour_plot;' + filename + ';' + x_axis + ';' + y_axis + ';' + plot_name)

###########################################################################
## \brief Counts the number of tasks in the queue.
## \return number of tasks in queue.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def task_count():
	return queue.task_count('jobs')