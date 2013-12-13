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
	## \param subsets - (= [(0, 0)]) a list of the start and end points (in bytes) of the subsets of data to be analysed
	## \return Returns DataReference object on success. Returns false on fail.
	## \note Will fail if no path is given.
	## \note Will fail if first value in the tuple is greater than the second.
	## \note Leaving set as default will include all of the available data in analysis.
	## \warning Does not check that the path for the data exists.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def __init__(	self,
					path,
					subsets = [(0, 0)]	):
		if path == None:
			return False
		for (x, y) in subsets:
			if x > y:
				return False
		## The path at which the data can be found.
		self.path = path
		## The subset of data being referenced.
		self.subset = subsets


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


## \brief Analysis id, responsible for holding information on a specific analysis and its users
class AnalysisID:
	
	###########################################################################
	## \brief Constructor for the AnalysisID object.
	## \param self - instance reference
	## \param analysis_id_number - the randomly assigned and unique identifier for this object
	## \param user_id_number - the id of the user associated with this analysis
	## \param data_ref - the DataReference object associated with this analysis
	## \param plugin_ref - the PluginReference object associated with this analysis
	## \return Returns AnalysisID object.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def __init__(	self,
					analysis_id_number,
					user_id_number,
					data_ref,
					plugin_ref	):
		## The unique id number used for referencing this analysis object.
		self.id_number = analysis_id_number
		## The list of users associated with this object. Initially only one user.
		self.users = [user_id_number]
		## The DataReference object for this analysis.
		self.data_ref = data_ref
		## The PluginReference object for this analysis.
		self.plugin_ref = plugin_ref
	
	###########################################################################
	## \brief Adds an additional user to the AnalysisID object
	## \param self - instance reference
	## \param user_id_number - the new user to be added to the object
	## \return Returns True on success, False if fails.
	## \note Will fail if the user already exists in the list of users.
	## \author swhitehouse@keesaco.com of Keesaco	
	###########################################################################
	def add_user(	self,
					user_id_number	):
		if user_id_number in self.users:
			return False
		self.users.append(user_id_number)
		return True
	
	###########################################################################
	## \brief Removes a user from the AnalysisID object
	## \param self - instance reference
	## \param user_id_number - the user to be removed from the object
	## \return Returns True on success, False if fails.
	## \note Will fail if the user does not exist in the list of users.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def remove_user(	self,
						user_id_number	):
		if user_id_number in self.users:
			self.users.remove(user_id_number)
			return True
		return False
	
	###########################################################################
	## \brief Checks for the number of occurrences of a specific user in the AnalysisID object.
	## \param self - instance reference
	## \param user_id_number - the user id to be checked for
	## \return Returns the number of occurrences of the chosen user in the AnalysisID object.
	## \note Due to error checking, this should only return 0 or 1.
	## \note Because of the above functionality, this can be user for error checking.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def check_for_user(	self,
						user_id_number	):
		return self.users.count(user_id_number)


## \brief Queue reference class holding a priority and an analysis id.
class QueueElement:

	###########################################################################
	## \brief Constructor for the QueueElement object.
	## \param self - instance reference
	## \param user_id - the id number for the original user
	## \param priority - (= 0) the user priority for the object
	## \return Returns QueueElement object.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def __init__(	self,
					user_id,
					priority = 1	):
		## The user_id list for the users performing this analysis.
		self.users = [user_id]
		if priority < 1:
			priority = 1
		## The priority list for this item in the queue.
		self.priorities = [priority]
		## The priority garnered through ageing by this object.
		self.total_priority = 0
	
	###########################################################################
	## \brief Ages the element by adding to its total priority.
	## \param self - instance reference
	## \return Does not return anything.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def age_element(	self	):
		self.total_priority += sum(self.priorities)
	
	###########################################################################
	## \brief Adds an additional user to the QueueElement object along with their priority.
	## \param self - instance reference
	## \param user_id - the new user to be added to the object
	## \param priority - (= 1) the priority associated with the new user
	## \return Returns True on success, False if fails.
	## \note Will fail if the user already exists in the list of users.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def add_user(	self,
					user_id,
					priority = 1	):
		if user_id in self.users:
			return False
		self.users.append(user_id)
		if priority < 1:
			priority = 1
		self.priorities.append(priority)
		return True
	
	###########################################################################
	## \brief Removes a user from the QueueElement object.
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
			del self.priorities[self.users.index(user_id)]
			self.users.remove(user_id)
			return True
		return False
	
	###########################################################################
	## \brief Checks how many users there are in a QueueElement object.
	## \param self - instance reference
	## \return Returns the number users. If fails, returns False.
	## \note The function will fail if the number of users is not equal to the number of priorities.
	## \note Because of the above functionality, this can be used for error checking.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################			
	def check_number_users(	self	):
		i = len(self.users)
		if i == len(self.priorities):
			return i
		return False

	###########################################################################
	## \brief A useful function for debugging which will print out the element information
	## \param self - instance reference
	## \param prefix - (= "")a string to be placed before each string printed by the function.
	## \return Returns nothing.
	## \note Due to the problems with printing to a console in multi-element programs, this function should only be user for debugging.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################		
	def print_element(	self,
						prefix = ""	):
		print (prefix + "Users: " + str(self.users))
		print (prefix + "Priorities: " + str(self.priorities))
		print (prefix + "Total Priority: " + str(self.total_priority))


## Schedule Queue class holding the dictionary of queue elements for the schedule.
class ScheduleQueue:

	from app.Analysis.Types import QueueElement
	
	###########################################################################
	## \brief Constructor for the ScheduleQueue object.
	## \param self - instance reference
	## \return Returns ScheduleQueue object.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def __init__(	self	):
		## A dictionary which will form the queue itself.
		self.elements = {}

	###########################################################################
	## \brief Ages each element in the queue.
	## \param self - instance reference
	## \return Does not return anything.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def age_queue(	self	):
		for analysis_id in self.elements:
			self.elements[analysis_id].age_element()

	###########################################################################
	## \brief Checks how many elements there are in the queue.
	## \param self - instance reference
	## \return Does not return anything.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def check_number_elements(	self	):
		return len(self.elements)

	###########################################################################
	## \brief Adds a user to a queue element if it exists, and makes a new one if it doesn't.
	## \param self - instance reference
	## \param analysis_id - the unique identifier for an analysis used as a key in the dictionary
	## \param user_id - the user to be added to the queue element
	## \param priority - the priority of the user to be added
	## \return Returns True on success, False if fails.
	## \note Will fail if the user already exists in the specific element.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def add_user_to_element(	self,
								analysis_id,
								user_id,
								priority = 1	):
		if analysis_id in self.elements:
			return self.elements[analysis_id].add_user(user_id, priority)
		self.elements[analysis_id] = QueueElement(user_id, priority)
		return True

	###########################################################################
	## \brief Removes a user from a queue element if it exists, removes the element if they were the last user.
	## \param self - instance reference
	## \param analysis_id - the unique identifier for an analysis used as a key in the dictionary
	## \param user_id - the user to be removed from the queue element
	## \return Returns True on success, False if fails.
	## \note Will fail if the user does not exist in the element, or if the element itself doesn't exist.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def remove_user_from_element(	self,
									analysis_id,
									user_id	):
		if analysis_id in self.elements:
			if self.elements[analysis_id].remove_user(user_id):
					if self.elements[analysis_id].check_number_users() == 0:
						del self.elements[analysis_id]
					return True
		return False

	###########################################################################
	## \brief Provides the caller with the element in the list with the highest priority.
	## \param self - instance reference
	## \return Returns the analysis_id of the highest priority element, or False if the queue is empty.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def next_element(	self	):
		if self.check_number_elements() == 0:
			return False
		analysis_id = max(iter(self.elements), key=(lambda key: self.elements[key].total_priority))
		del self.elements[analysis_id]
		return analysis_id
	
	###########################################################################
	## \brief Checks to see if an element is in the queue.
	## \param self - instance reference
	## \param analysis_id - the unique identifier for an analysis used as a key in the dictionary
	## \return Returns True if the element is in the queue, False if not.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def check_element(	self,
						analysis_id	):
		if analysis_id in self.elements:
			return True
		return False
	
	###########################################################################
	## \brief Checks to see how many times a user is listed next to a queue element
	## \param self - instance reference
	## \param user_id - the user to be checked for
	## \return Returns the number of times the user is listed under an element
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def check_user(	self,
					user_id	):
		occurances = 0
		for key in self.elements:
			if user_id in self.elements[key].users:
				occurances += 1
		return occurances

	###########################################################################
	## \brief A useful function for debugging which will print out the queue information
	## \param self - instance reference
	## \param prefix - (= "")a string to be placed before each string printed by the function.
	## \return Returns nothing.
	## \note Due to the problems with printing to a console in multi-element programs, this function should only be user for debugging.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################				
	def print_queue(	self,
						prefix = ""	):
		for key in self.elements:
			print (prefix + "Key: " + str(key))
			self.elements[key].print_element(prefix + "--> ")

