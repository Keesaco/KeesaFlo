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
	subprocess.call(['gsutil', 'cp', path_local, DEFAULT_BUCKET])

###########################################################################
## \brief Saves a visualisation of an fcs file
## \param name - name of fcs file to visualise
## \return returns True if successful else False
## \todo Implement return value.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def visualise(	name):
	subprocess.call(["Rscript", "visualise.r", name, name + '.png'])

###########################################################################
## \brief Saves a visualisation of an fcs file
## \param name - name of fcs file to visualise
## \param x_axis - name of x_axis desired
## \param y_axis - name of y_axis desired
## \return returns True if successful else False
## \todo Implement return value.
## \author hdoughty@keesaco.com of Keesaco
###########################################################################

def change_axis(name, x_axis, y_axis):
	subprocess.call(["Rscript", "axis.r", name, name + '1.png', x_axis, y_axis])

###########################################################################
## \brief Saves a visualisation of a gated fcs file
## \param name - name of fcs file to gate
## \pararm top_left_x - x coordinate of top left corner of rectangular gate
## \pararm top_left_y - y coordinate of top left corner of rectangular gate
## \pararm bottom_right_x - x coordinate of bottom right corner of rectangular gate
## \pararm bottom_right_y - y coordinate of bottom right corner of rectangular gate
## \return returns True if successful else False
## \note all parameters should be strings
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
def rect_gate(  name, gate_name, top_left_x, top_left_y, bottom_right_x, bottom_right_y):
	subprocess.call(["Rscript", "gate.r", name, gate_name, top_left_x, top_left_y, bottom_right_x, bottom_right_y])

###########################################################################
## \brief Saves a visualisation of a gated fcs file
## \param name - name of fcs file to gate
## \pararm mean_x - x coordinate of the mean of the gate
## \pararm mean_y - y coordinate of the mean of the gate
## \pararm a_x - x coordinate of the point further from the mean
## \pararm a_y - y coordinate of the point further from the mean
## \pararm b_x - x coordinate of the point closest to the mean
## \pararm b_y - y coordinate of the point closest to the mean
## \return returns True if successful else False
## \note all parameters should be strings
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
def oval_gate(name, gate_name, mean_x, mean_y, a_x, a_y, b_x, b_y):
	subprocess.call(["Rscript", "ovalgate.r", name, gate_name, mean_x, mean_y, a_x, a_y, b_x, b_y])

###########################################################################
## \brief Saves a visualisation of a gated fcs file
## \param name - name of fcs file to gate
## \pararm points - string of all the points which define the polygon gate
## \return returns True if successful else False
## \note all parameters should be strings
## \author hdoughty@keesaco.com of Keesaco
###########################################################################
def poly_gate(name, gate_name, points):
	subprocess.call(["Rscript", "polygate.r", name, gate_name, points])

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
