## \file shared/python/API/APIAnalysis.py
# \brief Defines the analysis API for analysing data. Built upon PALAnalysis for cross-platform support.
# \author swhitehouse@keesaco.com of Keesaco
# \author rmurley@keesaco.com of Keesaco

from PALAnalysis import *

## APIAnalysis
# Second tier API for analysis - utilises PAL for platform specific analysis
class APIAnalysis:

	## constructor
	# \author swhitehouse@keesaco.com of Keesaco
	def __init__(self):
		pass

	## queue_analysis requests that a new analysis be instantiated using a specified plugin and data-set
	# \param data_ref - reference to the data to be analysis
	# \param plugin_ref - reference to the plugin to be used for analysis
	# \param user_id - the id of the user starting the analysis
	# \param priority - a value determining the priority of the specific analysis
	# \return On fail, return false. On success, returns the analysis_id for the specific analysis request
	# \author swhitehouse@keesaco.com of Keesaco
	# \author rmurley@keesaco.com of Keesaco
	def queue_analysis(	data_ref,
						plugin_ref,
						user_id,
						priority	):
		pass

	## cancel_analysis requests that analysis instantiation is ended prematurely 
	# \param analysis_id - the id of the analysis that needs to be ended
	# \param user_id - the id of the user ending the analysis
	# \return If the user_id does not match the one stored in the analysis_id, return false. Else if analysis termination is successful, return True.
	# \author swhitehouse@keesaco.com of Keesaco
	# \author rmurley@keesaco.com of Keesaco
	def cancel_analysis(	analysis_id,
							user_id	):
		pass

	## change_priority_analysis requests that the priority of a currently running analysis instantiation is changed
	# \param analysis_id - the id of the analysis that is having its priority ended
	# \param user_id - the id of the user changing the priority
	# \param priority - a value determining the priority that the analysis needs to be changed to
	# \return If the user_id does not match the one stored in the analysis_id, return false. Else if analysis priority change is successful, return True.
	# \author swhitehouse@keesaco.com of Keesaco
	# \author rmurley@keesaco.com of Keesaco
	def change_priority_analysis(	analysis_id,
									user_id,
									priority	):
		pass

