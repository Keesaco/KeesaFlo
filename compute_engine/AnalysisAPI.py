###########################################################################
## \file compute/API/AnalysisAPI.py
## \brief Defines the analysis API for flow cytometry anlysis.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
## \package compute.API.AnalysisAPI
## \brief Provides methods for flow cytometry data analysis.
###########################################################################

###########################################################################
## \brief Loads an fcs file from the Datastore to local disk
## \param path_ds - datastore filepath to load from
## \param path_local - target local filepath to save to
## \param permissions - user attempting to perform access
## \return returns True if authourised else False
## \todo Stub: passes, needs implementing
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def load_fcs(	path_ds,
				path_local,
				permissions = None):
	pass

###########################################################################
## \brief Saves an fcs file from local disk to Datastore
## \param path_ds - target datastore filepath to save to
## \param path_local - local filepath to load from
## \param permissions - user attempting to perform access
## \return returns True if authourised else False
## \todo Stub: passes, needs implementing
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def save_fcs(	path_ds,
				path_local,
				permissions = None):
	pass

###########################################################################
## \brief Saves a visualisation of an fcs file as an image
## \param path_fcs - path of fcs file to visualise
## \param path_vis - target path of visualisation image
## \return returns True if successful else False
## \todo Stub: passes, needs implementing
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def visualise(	path_fcs,
				path_vis):
	pass

###########################################################################
## \brief Saves a visualisation image from local disk to Datastore
## \param path_ds - target datastore filepath to save to
## \param path_local - local filepath to load from
## \param permissions - user attempting to perform access
## \return returns True if authourised else False
## \todo Stub: passes, needs implementing
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def save_vis(	path_ds,
				path_local,
				permissions = None):
	pass
