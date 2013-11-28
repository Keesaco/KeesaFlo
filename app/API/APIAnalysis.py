## \file shared/python/API/APIAnalysis.py
# \brief Defines the analysis API for analysing data.
# \author swhitehouse@keesaco.com of Keesaco
# \author rmurley@keesaco.com of Keesaco

## \brief API for analysis - Manages requests to the Analysis API.
class APIAnalysis:

	## \brief Constructor for APIAnalysis.
	#  \param self - instance reference
	#  \return Returns the APIAnalysis instance.
	#  \author swhitehouse@keesaco.com of Keesaco
	def __init__(	self	):
		pass

	## \brief Is called to request that a new analysis using a specific plugin and data set be added to the scheduler.
	# \param data_ref - reference to the data to be analysis
	# \param plugin_ref - reference to the plugin to be used for analysis
	# \param user_id - the id of the user starting the analysis
	# \param priority - a value determining the priority of the specific analysis
	# \return On fail, return false. On success, returns the analysis_id for the specific analysis request.
	# \note user_id is used primarily to make sure that other users cannot mess with the original user's analysis.
	# \warning This function does not check that the user has permissions to perform the specified analysis. Nor does it check whether the analysis has already been performed.
	# \author swhitehouse@keesaco.com of Keesaco
	# \author rmurley@keesaco.com of Keesaco
	def queue_analysis(	data_ref,
						plugin_ref,
						user_id,
						priority	):
		pass
	
	## \brief Requests that the specific analysis instantiation is ended prematurely.
	# \param analysis_id - the id of the analysis that needs to be ended
	# \param user_id - the id of the user ending the analysis
	# \return If analysis termination is successful, return True. Else False.
	# \note May not actually cancel analysis, unless all users related to that analysis request for it to be cancelled.
	# \note Will fail if the user_id does not match stored values in the analysis_id.
	# \note Will fail if the analysis_id does not exist.
	# \author swhitehouse@keesaco.com of Keesaco
	# \author rmurley@keesaco.com of Keesaco
	def cancel_analysis(	analysis_id,
							user_id	):
		pass

	## \brief Requests that the current state of the analysis is checked.
	# \param analysis_id - the id of the analysis that is being checked
	# \param user_id - the id of the user checking the analysis
	# \return Returns information on the current state of the analysis. If failed, return False.
	# \note Will either return the analysis' position in the schedule, or the expected time remaining on the actual analysis.
	# \note Will fail if the user_id does not match stored values in the analysis_id.
	# \note Will fail if the analysis_id does not exist.
	# \author swhitehouse@keesaco.com of Keesaco
	# \author rmurley@keesaco.com of Keesaco
	def check_analysis(	analysis_id,
						user_id	):
		pass

