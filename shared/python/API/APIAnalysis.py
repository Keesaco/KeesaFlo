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
		
	## add_file creates a new file and optionally opens it in a given mode
	# \param data_ref - reference to the data to be analysis
	# \param plugin_ref - reference to the plugin to be used for analysis
	# \param user_id - the id of the user starting the analysis
	# \param priority - a value determining the priority of the specific analysis
	# \On fail, return false. On success, returns the analysis_id for the specific analysis request
	# \author swhitehouse@keesaco.com of Keesaco
	# \author rmurley@keesaco.com of Keesaco
	def queue_analysis(	data_ref,
						plugin_ref,
						user_id,
						priority	):
		pass