###########################################################################
## \file compute_engine/API/APIAnalysis.py
## \brief Defines the analysis API for flow cytometry analysis and visualisation.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
## \package compute_engine.API.APIAnalysis
## \brief Provides methods for flow cytometry data analysis and visualisation.
###########################################################################
import subprocess

RAW_BUCKET = 'gs://fc-raw-data/'
VIS_BUCKET = 'gs://fc-vis-data/'
INFO_BUCKET = 'gs://fc-info-data/'

###########################################################################
## \brief Loads an fcs file from the Datastore to local disk
## \param name - name of fcs file to load
## \param permissions - user attempting to perform access
## \return returns True if authourised else False
## \todo Modify to use Datastore API instead of gsutil. Implement permissions.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def load_fcs(	name,
				permissions = None):
	subprocess.call(['gsutil', 'cp', 'gs://fc-raw-data/' + name, name])
	return True

###########################################################################
## \brief Saves an fcs file from local disk to Datastore
## \param name - name of fcs file to save
## \param permissions - user attempting to perform access
## \return returns True if authourised else False
## \todo Modify to use Datastore API instead of gsutil. Implement permissions.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def save_fcs(	name,
				permissions = None):
	subprocess.call(['gsutil', 'cp', name, RAW_BUCKET])

###########################################################################
## \brief Saves a visualisation of an fcs file
## \param name - name of fcs file to visualise
## \return returns True if successful else False
## \return returns exit code from the subprocess
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def visualise(	name):
	return subprocess.call(["Rscript", "visualise.r", name, name + '.png', name + 'info.txt'])

###########################################################################
## \brief Saves a visualisation of an fcs file
## \param name - name of fcs file to visualise
## \param x_axis - name of x_axis desired
## \param y_axis - name of y_axis desired
## \return returns exit code from the subprocess
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
def change_axis(name, x_axis, y_axis):
	return subprocess.call(["Rscript", "axis.r", name, name + x_axis + y_axis + '.png', x_axis, y_axis])

###########################################################################
## \brief Saves a visualisation of an fcs file
## \param name - name of fcs file to visualise
## \param plot_name - name of image file to be created
## \param x_axis - name of x_axis desired
## \param y_axis - name of y_axis desired
## \return returns exit code from the subprocess
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
def dot_plot(name, plot_name, x_axis, y_axis):
	return subprocess.call(["Rscript", "graphs.r", name, plot_name, x_axis, y_axis, 'dot'])

###########################################################################
## \brief Saves a visualisation of an fcs file
## \param name - name of fcs file to visualise
## \param plot_name - name of image file to be created
## \param x_axis - name of x_axis desired
## \param y_axis - name of y_axis desired
## \return returns exit code from the subprocess
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
def contour_plot(name, plot_name, x_axis, y_axis):
	return subprocess.call(["Rscript", "graphs.r", name, plot_name, x_axis, y_axis, 'contour'])

###########################################################################
## \brief Saves a visualisation of a rectangular gated fcs file
## \param name - name of fcs file to gate
## \param gate_name - name of gate to be created
## \param top_left_x - x coordinate of top left corner of rectangular gate
## \param top_left_y - y coordinate of top left corner of rectangular gate
## \param bottom_right_x - x coordinate of bottom right corner of rectangular gate
## \param bottom_right_y - y coordinate of bottom right corner of rectangular gate
## \param reverse boolean representing whether cells in gate are kept or removed
## \param x_axis - name of x_axis desired
## \param y_axis - name of y_axis desired
## \return returns exit code from the subprocess
## \note all parameters should be strings
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
def rect_gate(  name, gate_name, top_left_x, top_left_y, bottom_right_x, bottom_right_y, reverse, x_axis, y_axis):
	return subprocess.call(["Rscript", "gate.r", name, gate_name, "rect", reverse, top_left_x, top_left_y, bottom_right_x, bottom_right_y, x_axis, y_axis])

###########################################################################
## \brief Saves a visualisation of an oval gated fcs file
## \param name - name of fcs file to gate
## \param gate_name - name of gate to be created
## \param mean_x - x coordinate of the mean of the gate
## \param mean_y - y coordinate of the mean of the gate
## \param a_x - x coordinate of the point further from the mean
## \param a_y - y coordinate of the point further from the mean
## \param b_x - x coordinate of the point closest to the mean
## \param b_y - y coordinate of the point closest to the mean
## \param reverse boolean representing whether cells in gate are kept or removed
## \param x_axis - name of x_axis desired
## \param y_axis - name of y_axis desired
## \return returns exit code from the subprocess
## \note all parameters should be strings
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
def oval_gate(name, gate_name, mean_x, mean_y, a_x, a_y, b_x, b_y, reverse, x_axis, y_axis):
	return subprocess.call(["Rscript", "gate.r", name, gate_name, "oval", reverse, mean_x, mean_y, a_x, a_y, b_x, b_y, x_axis, y_axis])

###########################################################################
## \brief Saves a visualisation of a polygon gated fcs file
## \param name - name of fcs file to gate
## \param gate_name - name of gate to be created
## \param points - string of all the points which define the polygon gate
## \param reverse boolean representing whether cells in gate are kept or removed
## \param x_axis - name of x_axis desired
## \param y_axis - name of y_axis desired
## \return returns exit code from the subprocess
## \note all parameters should be strings
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
def poly_gate(name, gate_name, points, reverse, x_axis, y_axis):
	return subprocess.call(["Rscript", "gate.r", name, gate_name, "poly", reverse, points, x_axis, y_axis])

###########################################################################
## \brief Saves a visualisation of a boolean gated fcs file
## \param name - name of fcs file to gate
## \param gate_name - name of gate to be created
## \param boolean_op - boolean operator to be used to join the two gates: 'and' or 'or'
## \param gate1_type - type of first gate to be created
## \param points1 - string of all the points which define the first gate
## \param reverse1 - boolean representing whether cells in gate 1 are kept or removed
## \param gate2_type - type of second gate to be created
## \param points2 - string of all the points which define the second gate
## \param reverse2 - boolean representing whether cells in gate 2 are kept or removed
## \param gate1_x_axis - name of x_axis desired for first gate, also used for visualisation
## \param gate1_y_axis - name of y_axis desired for first gate, also used for visualisation
## \param gate2_x_axis - name of x_axis desired for second gate
## \param gate2_y_axis - name of y_axis desired for second gate
## \return returns exit code from the subprocess
## \note all parameters should be strings
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
def bool_gate(name, gate_name, boolean_op, gate1_type, points1, reverse1, gate2_type, 
	points2, reverse2, gate1_x_axis, gate1_y_axis, gate2_x_axis, gate2_y_axis):
	return subprocess.call(["Rscript", "boolean.r", name, gate_name, boolean_op, gate1_type, 
		points1, reverse1, gate2_type, points2, reverse2, gate1_x_axis, gate1_y_axis, gate2_x_axis, gate2_y_axis])

###########################################################################
## \brief Saves a visualisation of an fcs file gated using a normal distribution
## \param name - name of fcs file to gate
## \param gate_name - name of gate to be created
## \param reverse boolean representing whether cells in gate are kept or removed
## \param x_axis - name of x_axis desired
## \param y_axis - name of y_axis desired
## \param scale_factor - number of standard deviations used for data selection
## \return returns exit code from the subprocess
## \note all parameters should be strings
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
def norm_gate(name, gate_name, reverse, x_axis, y_axis, scale_factor):
	return subprocess.call(["Rscript", "norm_gate.r", name, gate_name, reverse, x_axis, y_axis, scale_factor])

###########################################################################
## \brief Saves a visualisations fcs file split up into four quadrants
## \param name - name of fcs file to gate
## \param x_coord - x coordinate the quadrant split is based upon
## \param y_coord - y coordinate the quadrant split is based upon
## \param quad1_name - desired name of top right quadrant
## \param quad2_name - desired name of top left quadrant
## \param quad3_name - desired name of bottom right quadrant
## \param quad4_name - desired name of bottom left quadrant
## \param x_axis - name of x_axis desired
## \param y_axis - name of y_axis desired
## \return returns exit code from the subprocess
## \note all parameters should be strings
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
def quad_gate(name, x_coord, y_coord, quad1_name, quad2_name, quad3_name, quad4_name, x_axis, y_axis):
	return subprocess.call(["Rscript", "quad_gate.r", name, x_coord, y_coord, quad1_name, quad2_name, 
		quad3_name, quad4_name, x_axis, y_axis])

###########################################################################
## \brief Saves a visualisation of an fcs file gated using a normal distribution
## \param name - name of fcs file to gate
## \param cluster_name - name of clusters to be created in one string seperated by spaces
## \param number_clusters - number of clusters desired
## \param x_axis - name of x_axis desired
## \param y_axis - name of y_axis desired
## \return returns exit code from the subprocess
## \note all parameters should be strings
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
def kmeans_gate(name, cluster_names, number_clusters, x_axis, y_axis):
	return subprocess.call(["Rscript", "kmeans.r", name, cluster_names, number_clusters, x_axis, y_axis])

###########################################################################
## \brief Saves a visualisation image from local disk to Datastore
## \param name - name of image file to save
## \param permissions - user attempting to perform access
## \return returns True if authourised else False
## \todo Modify to use Datastore API instead of gsutil. Implement permissions.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def save_vis(	name,
				permissions = None):
	subprocess.call(['gsutil', 'cp', name, VIS_BUCKET])
	return True

###########################################################################
## \brief Saves a text file containing gating info from local disk to Datastore
## \param name - name of text file to save
## \param permissions - user attempting to perform access
## \return returns True if authourised else False
## \author hdoughty@keesaco.com of Keesaco
###########################################################################

def save_info(	name,
				permission = None):
	subprocess.call(['gsutil', 'cp', name, INFO_BUCKET])
	return True
