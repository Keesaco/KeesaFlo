###########################################################################
## \file app/Analysis/Types.py
## \brief Contains all analysis types.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################
## \package app.Analysis.Types
## \brief Provides all type classes associated with analysis.
###########################################################################

import random

## \brief Analysis request, responsible for holding information on a specific analysis and its users
class AnalysisRequest:
	
	###########################################################################
	## \brief Constructor for the AnalysisRequest object.
	## \param self - instance reference
	## \param file_location - location of the file to be analysed
	## \return Returns AnalysisRequest object.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def __init__(	self,
					file_location	):
		## The DataLocation object for this analysis.
		self.file_location = file_location
		## A bool showing whether the object is in the queue.
		self.in_queue = False
		## A bool showing whether the object is being analysed.
		self.being_analysed = False
	
	###########################################################################
	## \brief Changes the state of the AnalysisRequest object.
	## \param self - instance reference
	## \param in_queue - whether the object is in the queue or not
	## \param being_analysed - whether the object is being analysed or not
	## \return Returns True on successful change of state, False on fail.
	## \note This function will fail if both in_queue and being_analysed are True.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def change_state(	self,
						in_queue = False,
						being_analysed = False	):
		if in_queue and being_analysed:
			return False
		self.in_queue = in_queue
		self.being_analysed = being_analysed
		return True
	
	###########################################################################
	## \brief Comparison for AnalysisRequest objects.
	## \param self - instance reference
	## \param data_location - the DataLocation object to be compared
	## \param plugin_location - the PluginLocation object to be compared
	## \return Returns True if the objects match, False if not.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################		
	def compare_request(	self,
							data_location,
							plugin_location	):
		if self.plugin_location.compare_plugin(plugin_location):
			if self.data_location.compare_data(data_location):
				return True
		return False
	
	###########################################################################
	## \brief A useful function for debugging which will print out the request information.
	## \param self - instance reference
	## \param prefix - (= "")a string to be placed before each string printed by the function.
	## \return Returns nothing.
	## \note Due to the problems with printing to a console in multi-element programs, this function should only be user for debugging.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################	
	def print_request(	self,
						prefix = ""	):
		print (prefix + "Users: " + str(self.users))
		print (prefix + "In Queue?: " + str(self.in_queue))
		print (prefix + "Being Analysed?: " + str(self.being_analysed))
		print (prefix + "Data:")
		self.data_location.print_data(prefix + "> ")
		print (prefix + "Plugin:")
		self.plugin_location.print_plugin(prefix + "> ")
			

## \brief Dictionary for all current Analysis requests.
class RequestList:
	
	###########################################################################
	## \brief Constructor for the RequestList object.
	## \param self - instance reference
	## \return Returns RequestList object.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def __init__(	self	):
		## A dictionary will will make up the list itself.
		self.requests = {}
	
	###########################################################################
	## \brief Subscribes a user to an analysis request using the specified data and plugin.
	## \param self - instance reference
	## \param user_id - the user to be subscribed
	## \param data_location - the DataLocation object to be used
	## \param plugin_location - the PluginLocation object to be used
	## \return Returns the analysis_id of the object created or added to, else False if fails.
	## \note Will fail if the user is already subscribed to the analysis object.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def subscribe_user(	self,
						user_id,
						data_location,
						plugin_location	):
		for analysis_id in self.requests:
			if self.requests[analysis_id].compare_request(data_location, plugin_location):
				if not self.requests[analysis_id].add_user(user_id) == False:
					return analysis_id
				return False
		analysis_id = random.randint(10000000, 99999999)
		while analysis_id in self.requests:
			analysis_id = random.randint(10000000, 99999999)
		self.requests[analysis_id] = AnalysisRequest(user_id, data_location, plugin_location)
		return analysis_id
		
	###########################################################################
	## \brief Unsubscribes a user from an analysis request using the analysis id.
	## \param self - instance reference
	## \param user_id - the user to be unsubscribed
	## \param analysis_id - the identifier of the object for the user to be removed from.
	## \return Returns True on success, else False if fails.
	## \note Will fail if the user is not subscribed to the object, or the object does not exist.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def unsubscribe_user(	self,
							analysis_id,
							user_id	):
		if analysis_id in self.requests:
			if self.requests[analysis_id].remove_user(user_id):
				if self.requests[analysis_id].check_number_users() == 0:
					del self.requests[analysis_id]
				return True
		return False
	
	###########################################################################
	## \brief Checks how many requests there are in the queue.
	## \param self - instance reference
	## \return Returns the number of requests there are in the list.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def check_number_requests(	self	):
		return len(self.requests)
	
	###########################################################################
	## \brief Changes the state of an AnalysisRequest object.
	## \param self - instance reference
	## \param analysis_id - the id of the request to be changed
	## \param in_queue - whether the object is in the queue or not
	## \param being_analysed - whether the object is being analysed or not
	## \return Returns True on successful change of state, False on fail.
	## \note This function will fail if both in_queue and being_analysed are True.
	## \note This function will also fail if the analysis_id does not exist in requests.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################	
	def change_state_request(	self,
								analysis_id,
								in_queue,
								being_analysed	):
		if analysis_id in self.requests:
			return self.requests[analysis_id].change_state(in_queue, being_analysed)
		return False

	###########################################################################
	## \brief A useful function for debugging which will print out the list information for all requests.
	## \param self - instance reference
	## \param prefix - (= "")a string to be placed before each string printed by the function.
	## \return Returns nothing.
	## \note Due to the problems with printing to a console in multi-element programs, this function should only be user for debugging.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################	
	def print_list(	self,
					prefix = ""	):
		for analysis_id in self.requests:
			print (prefix + "Request: " + str(analysis_id))
			self.requests[analysis_id].print_request(prefix + "-> ")
			print (prefix + "--------------------")
	

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
	## \param prefix - (= "") a string to be placed before each string printed by the function.
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
	## \return Returns the number of elements in the queue.
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
		for analysis_id in self.elements:
			if user_id in self.elements[analysis_id].users:
				occurances += 1
		return occurances

	###########################################################################
	## \brief A useful function for debugging which will print out the queue information
	## \param self - instance reference
	## \param prefix - (= "") a string to be placed before each string printed by the function.
	## \return Returns nothing.
	## \note Due to the problems with printing to a console in multi-element programs, this function should only be user for debugging.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################				
	def print_queue(	self,
						prefix = ""	):
		for analysis_id in self.elements:
			print (prefix + "Element: " + str(analysis_id))
			self.elements[analysis_id].print_element(prefix + "--> ")

