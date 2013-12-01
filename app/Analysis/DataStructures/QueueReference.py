###########################################################################
## \file app/Analysis/DataStructures/QueueReference.py
## \brief Contains the queue reference class.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################
## \package app.Analysis.DataStructures.QueueReference
## \brief Provides a reference to a specific analysis id which can be stored in a priority queue.
###########################################################################

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
					priority = 0	):
		## The id number for the specific analysis.
		self.id_number = id_number
		## The user_id list for the users performing this analysis.
		self.users = [user_id]
		if priority < 0:
			priority = 0
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

