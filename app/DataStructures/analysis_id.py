## \file app/DataStructures/analysis_id.py
# \brief Contains the analysis id class
# \author swhitehouse@keesaco.com of Keesaco

## \brief Analysis id, responsible for holding information on a specific analysis and its users
class analysis_id:
	
	## \brief Constructor for the analysis_id object.
	# \param self - instance reference
	# \param analysis_id_number - the randomly assigned and unique identifier for this object
	# \param user_id - the id of the user associated with this analysis
	# \param data_ref - the data_ref object associated with this analysis
	# \param plugin_ref - the plugin_ref object associated with this analysis
	# \return Returns analysis_id object.
	# \author swhitehouse@keesaco.com of Keesaco
	def __init__(self, analysis_id_number, user_id, data_ref, plugin_ref):
		## The unique id number used for referencing this analysis object.
		self.analysis_id_number = analysis_id_number
		## The list of users associated with this object.
		self.user_id = [user_id]
		## The data_ref object for this analysis.
		self.data_ref = data_ref
		## The plugin_ref object for this analysis.
		self.plugin_ref = plugin_ref
		return self

