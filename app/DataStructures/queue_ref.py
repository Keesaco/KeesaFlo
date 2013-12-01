###########################################################################
## \file app/DataStructures/queue_ref.py
## \brief Contains the queue reference class.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################
## \package app.DataStructures.queue_ref
## \brief Provides a queue reference class
## \todo The name of this package/file violates our naming convention, should be fixed
###########################################################################

## \brief Queue reference class holding a priority and an analysis id.
class queue_ref:

	###########################################################################
	## \brief Constructor for the queue_ref object.
	## \param self - instance reference
	## \param analysis_id_number - the id number for the specific analysis
	## \param user_id - the id number for the original user
	## \param priority - (= 0) the user priority for the object
	## \return Returns queue_ref object.
	## \warning Does not check that the analysis_id_number references anything.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def __init__(self, analysis_id_number, user_id, priority = 0):
		## The id number for the specific analysis.
		self.analysis_id_number = analysis_id_number
		## The user_id list for the users performing this analysis.
		self.users = [user_id]
		if priority < 0:
			priority = 0
		## The priority list for this item in the queue.
		self.priorities = [priority]
		## The priority garnered through aging by this object.
		self.total_priority = 0
		return self
	
	###########################################################################
	## \brief Ages the reference allowing for even the lowest priority references to have a chance at being processed.
	## \param self - instance reference
	## \return Returns True.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def age_reference(self):
		self.total_priority += sum(self.prioritys)
		return True
	
	###########################################################################
	## \brief Adds an additional user to the queue_ref object along with their associated priority
	## \param self - instance reference
	## \param user_id - the new user to be added to the object
	## \param priority - the priority associated with the new user
	## \return Returns True on success, False if fails.
	## \note Will fail if the user already exists in the list of users.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def add_user(self, user_id, priority):
		if user_id in self.users:
			return False
		self.users.append(user_id)
		self.priorities.append(priority)
		return True
	
	###########################################################################
	## \brief Removes a user from the queue_ref object
	## \param self - instance reference
	## \param user_id - the user to be removed from the object
	## \return Returns True on success, False if fails.
	## \note Will fail if the user does not exist in the list of users.
	## \note Will also remove the priority associated with the old user.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def remove_user(self, user_id):
		if user_id in self.users:
			self.priorities.remove(self.users.index(user_id))
			self.users.remove(user_id)
			return True
		return False

