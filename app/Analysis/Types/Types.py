###########################################################################
## \file app/Analysis/Types.py
## \brief Contains all analysis types.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################
## \package app.Analysis.Types
## \brief Provides all type classes associated with analysis.
###########################################################################


## \brief Data reference class for holding information about a portion of a data set.
class DataReference:
	###########################################################################
	## \brief Constructor for the DataReference object.
	## \param self - instance reference
	## \param path - path through which the data can be located in the data store
	## \param start - (= 0) the start point of the data to be included in analysis
	## \param end - (= 0) the end point of the data to be included in analysis
	## \return Returns DataReference object on success. Returns false on fail.
	## \note Will fail if no path is given.
	## \note Will fail if end is less than start.
	## \note Setting both start and end to 0 (as is default) will include all of the available data in analysis.
	## \warning Does not check that the path for the data exists.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def __init__(	self,
					path,
					start = 0,
					end = 0	):
		if start > end || start == end != 0 || path == None:
			return False
		## The path at which the data can be found.
		self.path = path
		## The start of the data set to be used (in bytes).
		self.start_set = start
		## The end of the data set to be used (in bytes).
		self.end_set = end
		return self


## \brief Plugin reference class for holding information about the location of a plugin.
class PluginReference:
	
	###########################################################################
	## \brief Constructor for the PluginReference object.
	## \param self - instance reference
	## \param path - path through which the plugin can be located in the data store
	## \return Returns PluginReference object on success. Returns false on fail.
	## \note Will fail if no path is given.
	## \warning Does not check that the path for the plugin exists.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def __init__(	self,
					path	):
		if path == None:
			return False
		## The path at which the plugin can be found.
		self.path = path
		return self


## \brief Analysis id, responsible for holding information on a specific analysis and its users
class AnalysisID:
	
	###########################################################################
	## \brief Constructor for the AnalysisID object.
	## \param self - instance reference
	## \param id_number - the randomly assigned and unique identifier for this object
	## \param user_id - the id of the user associated with this analysis
	## \param data_ref - the DataReference object associated with this analysis
	## \param plugin_ref - the PluginReference object associated with this analysis
	## \return Returns AnalysisID object.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def __init__(self, id_number, user_id, data_ref, plugin_ref):
		## The unique id number used for referencing this analysis object.
		self.id_number = id_number
		## The list of users associated with this object.
		self.users = [user_id]
		## The DataReference object for this analysis.
		self.data_ref = data_ref
		## The PluginReference object for this analysis.
		self.plugin_ref = plugin_ref
		return self
	
	###########################################################################
	## \brief Adds an additional user to the AnalysisID object
	## \param self - instance reference
	## \param user_id - the new user to be added to the object
	## \return Returns True on success, False if fails.
	## \note Will fail if the user already exists in the list of users.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def add_user(self, user_id):
		if user_id in self.users:
			return False
		self.users.append(user_id)
		return True
	
	###########################################################################
	## \brief Removes a user from the AnalysisID object
	## \param self - instance reference
	## \param user_id - the user to be removed from the object
	## \return Returns True on success, False if fails.
	## \note Will fail if the user does not exist in the list of users.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def remove_user(self, user_id):
		if user_id in self.users:
			self.users.remove(user_id)
			return True
		return False
	
	###########################################################################
	## \brief Checks for the number of occurrences of a specific user in the AnalysisID object.
	## \param self - instance reference
	## \param user_id - the user id to be checked for
	## \return Returns the number of occurrences of the chosen user in the AnalysisID object.
	## \note Due to error checking, this should only return 0 or 1.
	## \note Because of the above functionality, this can be user for error checking.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def check_for_user(self, user_id):
		return self.users.count(user_id)


## \brief Queue reference class holding a priority and an analysis id.
class QueueReference:

	###########################################################################
	## \brief Constructor for the QueueReference object.
	## \param self - instance reference
	## \param id_number - the id number for the specific analysis
	## \param user_id - the id number for the original user
	## \param priority - (= 0) the user priority for the object
	## \return Returns QueueReference object.
	## \warning Does not check that the analysis_id_number references anything.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def __init__(	self,
					id_number,
					user_id,
					priority = 1	):
		## The id number for the specific analysis.
		self.id_number = id_number
		## The user_id list for the users performing this analysis.
		self.users = [user_id]
		if priority < 1:
			priority = 1
		## The priority list for this item in the queue.
		self.priorities = [priority]
		## The priority garnered through ageing by this object.
		self.total_priority = 0
		return self
	
	###########################################################################
	## \brief Ages the reference allowing for low priority references to be processed.
	## \param self - instance reference
	## \return Returns True.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def age_reference(	self	):
		self.total_priority += sum(self.priorities)
		return True
	
	###########################################################################
	## \brief Adds an additional user to the QueueReference object along with their priority.
	## \param self - instance reference
	## \param user_id - the new user to be added to the object
	## \param priority - the priority associated with the new user
	## \return Returns True on success, False if fails.
	## \note Will fail if the user already exists in the list of users.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def add_user(	self,
					user_id,
					priority	):
		if user_id in self.users:
			return False
		self.users.append(user_id)
		self.priorities.append(priority)
		return True
	
	###########################################################################
	## \brief Removes a user from the QueueReference object.
	## \param self - instance reference
	## \param user_id - the user to be removed from the object
	## \return Returns True on success, False if fails.
	## \note Will fail if the user does not exist in the list of users.
	## \note Will also remove the priority associated with the old user.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def remove_user(	self,
						user_id	):
		if user_id in self.users:
			self.priorities.remove(self.users.index(user_id))
			self.users.remove(user_id)
			return True
		return False

	###########################################################################
	## \brief Checks for a user from the QueueReference object.
	## \param self - instance reference
	## \param user_id - the user to be checked for in the object
	## \return Returns the number of occurrences of the user.
	## \note Due to error checking, this should only return 0 or 1.
	## \note Because of the above functionality, this can be used for error checking.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################		
	def check_for_user(	self,
						user_id	):
		return self.users.count(user_id)

	###########################################################################
	## \brief Checks how many users there are in a QueueReference object.
	## \param self - instance reference
	## \return Returns the number users. If fails, returns False.
	## \note The function will fail if the number of users is not equal to the number of priorities.
	## \note Because of the above functionality, this can be used for error checking.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################		
	def check_user_amount(	self	):
		i = self.users.length()
		if i == self.priorities.length()
			return i
		return False

