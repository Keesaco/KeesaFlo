###########################################################################
## \file app/API/APIAnalysis.py
## \brief Defines the analysis API for analysing data.
## \author swhitehouse@keesaco.com of Keesaco
## \author rmurley@keesaco.com of Keesaco
###########################################################################
## \package app.API.APIAnalysis
## \brief Provides an API for accessing the analysis plugin management.
###########################################################################

# from app.Analysis.Manager import AnalysisManager
from Analysis.ComputeEngine.GCEManager import GCEManager

## !!TEMP!! The manager instance for Compute Engine.
gce_manager = GCEManager()

###########################################################################
## \brief Requests that a new analysis task be created.
## \param file_location - the location of the file to be analysed
## \return Returns analysis_id on success, False on fail.
## \author swhitehouse@keesaco.com of Keesaco
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def add_analysis_task(	file_location	):
	# !!TEMP!! Uses the file location to start an instance on Compute Engine.
	
	return gce_manager.start_instance_pd("default", file_location)
	

###########################################################################
## \brief Requests that an exists analysis task be deleted.
## \param analysis_id - the id of the analysis to be deleted
## \return Returns True on success, False on fail.
## \author swhitehouse@keesaco.com of Keesaco
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def remove_analysis_task(	analysis_id	):
	# !!TEMP!! Uses the file location to end an instance on Compute Engine.
	return gce_manager.terminate_instance_pd(analysis_id)

###########################################################################
## \brief Requests that the state of the analysis task be checked.
## \param analysis_id - the id of the analysis that is being checked
## \return Returns information on the state of the analysis (details in notes).
## \note True if the task is being analysed currently.
## \note An integer (>1) of the task's position in the queue.
## \note False if the analysis_id does not exist (i.e. the task does not exist).
## \author swhitehouse@keesaco.com of Keesaco
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def check_analysis_task(	analysis_id	):
	# !!TEMP!! Always returns True.
	return True

