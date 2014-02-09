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
	subprocess.call(["Rscript", "visualise.r", name + '.fcs', name + '.png'])

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
