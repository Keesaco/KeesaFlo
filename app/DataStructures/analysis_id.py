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
		self.users = [user_id]
		## The data_ref object for this analysis.
		self.data_ref = data_ref
		## The plugin_ref object for this analysis.
		self.plugin_ref = plugin_ref
		return self
	
	## \brief Adds an additional user to the analysis id object
	# \param self - instance reference
	# \param user_id - the new user to be added to the object
	# \return Returns True on success, False if fails.
	# \note Will fail if the user already exists in the list of users.
	# \author swhitehouse@keesaco.com of Keesaco
	def add_user(self, user_id):
		if user_id in self.users:
			return False
		self.users.append(user_id)
		return True
	
	## \brief Removes a user from the analysis id object
	# \param self - instance reference
	# \param user_id - the user to be removed from the object
	# \return Returns True on success, False if fails.
	# \note Will fail if the user does not exist in the list of users.
	# \author swhitehouse@keesaco.com of Keesaco
	def remove_user(self, user_id):
		if user_id in self.users:
			self.users.remove(user_id)
			return True
		return False
	
	## \brief Checks for the number of occurrences of a specific user in the analysis object.
	# \param self - instance reference
	# \param user_id - the user id to be checked for
	# \return Returns the number of occurrences of the chosen user in the analysis object.
	# \note Due to error checking, this should only return 0 or 1.
	# \note Because of the above functionality, this can be user for error checking.
	# \author swhitehouse@keesaco.com of Keesaco
	def check_for_user(self, user_id):
		return self.users.count(user_id)
		

