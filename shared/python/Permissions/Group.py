## \file shared/python/permissions/Group.py
# contains the group class

## \class Group
# \brief Group class for holding information about a usergroup
class Group:
	group_name = "" ## Name of the user group
	
	## constructor - creates a Group instance with a given groupname
	# \param self - instance reference
	# \param name - (= None) [String] name of user group
	# \return Group instance
	# \author jmccrea@keesaco.com of Keesaco
	def __init__(self, name = None):
		self.group_name = name