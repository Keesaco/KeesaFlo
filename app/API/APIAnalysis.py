###########################################################################
## \file app/API/APIAnalysis.py
## \brief Defines the analysis API for analysing data.
## \author swhitehouse@keesaco.com of Keesaco
## \author rmurley@keesaco.com of Keesaco
###########################################################################
## \package app.API.APIAnalysis
## \brief Provides an API for accessing the analysis plugin management.
###########################################################################

from app.Analysis.Manager import AnalysisManager

###########################################################################
## \brief Is called to request that a new analysis be created or added to.
## \param user_id - the id of the user
## \param priority - a value determining the priority of the user
## \param data_location - the DataLocation object to be used in analysis
## \param plugin_location - the PluginLocation object to be used in analysis
## \return On fail, return false. On success, returns the analysis_id_number for the specific analysis request.
## \note user_id is used primarily to make sure that other users cannot mess with the original user's analysis.
## \warning This function does not check that the user has permissions to perform the specified analysis. Nor does it check whether the analysis has already been performed.
## \author swhitehouse@keesaco.com of Keesaco
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def add_user_analysis(	user_id,
						priority,
						data_location,
						plugin_location	):
	return AnalysisManager.subscribe_user_analysis(user_id, priority, data_location, plugin_location)
	

###########################################################################
## \brief Requests that a user is removed from an analysis request.
## \param analysis_id - the id of the analysis to be removed from
## \param user_id - the id of the user to be removed
## \return Returns True on success, False if fails.
## \note Will fail if the user_id does not match stored values in the analysis_id.
## \note Will fail if the analysis_id does not exist.
## \author swhitehouse@keesaco.com of Keesaco
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def remove_user_analysis(	analysis_id,
							user_id	):
	return AnalysisManager.unsubscribe_user_analysis(analysis_id, user_id)

###########################################################################
## \brief Requests that the current state of the analysis is checked.
## \param analysis_id - the id of the analysis that is being checked
## \param user_id - the id of the user checking the analysis
## \return Returns information on the current state of the analysis. If failed, return False.
## \note Will either return the analysis' position in the schedule, or the expected time remaining on the actual analysis.
## \note Will fail if the user_id does not match stored values in the analysis_id.
## \note Will fail if the analysis_id does not exist.
## \author swhitehouse@keesaco.com of Keesaco
## \author rmurley@keesaco.com of Keesaco
###########################################################################
def check_analysis(	analysis_id,
					user_id	):
	return AnalysisManager.check_analysis(analysis_id, user_id)

