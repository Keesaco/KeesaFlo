## \file shared/python/API/APIAnalysis.py
# \brief Defines the analysis API for analysing data. Built upon PALAnalysis for cross-platform support.
# \author swhitehouse@keesaco.com of Keesaco
# \author rmurley@keesaco.com of Keesaco

from PALAnalysis import *

## \brief Second tier API for analysis - utilises PAL for platform specific analysis
class APIAnalysis:

	## \brief Constructor for API
	# \param self - instance reference
	# \return APIAnalysis instance
	# \author swhitehouse@keesaco.com of Keesaco
	def __init__(	self	):
		pass

	## \brief Queue_analysis requests that a new analysis be instantiated using a specified plugin and data-set
	# \param data_ref - reference to the data to be analysis
	# \param plugin_ref - reference to the plugin to be used for analysis
	# \param user_id - the id of the user starting the analysis
	# \param priority - a value determining the priority of the specific analysis
	# \return On fail, return false. On success, returns the analysis_id for the specific analysis request
	# \warning This function does not check that the user has permissions to perform the specified analysis. Nor does it, for the time being, check whether the analysis has already been performed.
	# \author swhitehouse@keesaco.com of Keesaco
	# \author rmurley@keesaco.com of Keesaco
	def queue_analysis(	data_ref,
						plugin_ref,
						user_id,
						priority	):
		pass

	## \brief Cancel_analysis requests that the specific analysis instantiation is ended prematurely 
	# \param analysis_id - the id of the analysis that needs to be ended
	# \param user_id - the id of the user ending the analysis
	# \return If failed, return false. Else if analysis termination is successful, return True.
	# \note If the user_id does not match the one paired with the analysis_id on file, this function will fail.
	# \author swhitehouse@keesaco.com of Keesaco
	# \author rmurley@keesaco.com of Keesaco
	def cancel_analysis(	analysis_id,
							user_id	):
		pass

	## \brief Change_priority_analysis requests that the priority of a currently running analysis instantiation is changed
	# \param analysis_id - the id of the analysis that is having its priority changed
	# \param user_id - the id of the user changing the priority
	# \param priority - a value determining the priority that the analysis needs to be changed to
	# \return If failed, return false. Else if analysis priority change is successful, return True.
	# \note If the user_id does not match the one stored in the analysis_id then this function will fail.
	# \author swhitehouse@keesaco.com of Keesaco
	# \author rmurley@keesaco.com of Keesaco
	def change_priority_analysis(	analysis_id,
									user_id,
									priority	):
		pass

	## \brief check_analysis requests that the current state of the analysis is checked
	# \param analysis_id - the id of the analysis that is being checked
	# \param user_id - the id of the user checking the analysis
	# \returns If failed, return false. Else if the user is in the allowed checking list, then information on the current state of the analysis will be returned.
	# \note Unknown contents of the information at this time.
	# \author swhitehouse@keesaco.com of Keesaco
	# \author rmurley@keesaco.com of Keesaco
	def check_analysis(	analysis_id,
						user_id	):
		pass
		
	## \brief Change_user_analysis changes the owner of the current analysis instantiation
	# \param analysis_id - the id of the analysis that is being passed on
	# \param user_id - the id of the user requesting the change
	# \param new_user_id - the id of the user the analysis instantiation is being transferred to.
	# \return If failed, return false. Else if analysis user change is successful, return True.
	# \note If the user_id does not match the one stored in the analysis_id then this function will fail. The new_user_id will be checked to make sure they have permissions for the data and the plugin with the function failing if they do not. Priority will also be modified to be in keeping with the new user's own priority.
	# \author swhitehouse@keesaco.com of Keesaco
	# \author rmurley@keesaco.com of Keesaco
	def change_user_analysis(	analysis_id,
								user_id,
								new_user_id	):
		pass

