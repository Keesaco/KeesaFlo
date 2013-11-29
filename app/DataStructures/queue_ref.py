## \file app/DataStructures/queue_ref.py
# \brief Contains the queue reference class.
# \author swhitehouse@keesaco.com of Keesaco

## \brief Queue reference class holding a priority and an analysis id.
class queue_ref:
	
	## \brief Constructor for the queue_ref object.
	# \param self - instance reference
	# \param analysis_id_number - the id number for the specific analysis
	# \param user_id - the id number for the original user
	# \param priority - (= 0) the user priority for the object
	# \return Returns queue_ref object.
	# \warning Does not check that the analysis_id_number references anything.
	# \author swhitehouse@keesaco.com of Keesaco
	def __init__(self, analysis_id_number, user_id, priority = 0):
		## The id number for the specific analysis.
		self.analysis_id_number = analysis_id_number
		## The user_id list for the users performing this analysis.
		self.user_id = [user_id]
		if priority < 0:
			priority = 0
		## The priority list for this item in the queue.
		self.priority = [priority]
		## The priority garnered through aging by this object.
		self.add_priority = 0
		return self

