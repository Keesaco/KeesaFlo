## \file app/permissions/Group.py
# \brief contains the group class
# \author jmccrea@keesaco.com of Keesaco

## \brief Group class for holding information about a usergroup
class Group:
	
	## name of the use group
	group_name = ""
	
	## \brief constructor - creates a Group instance with a given groupname
	# \param self - instance reference
	# \param name - (= None) [String] name of user group
	# \return Group instance
	# \author jmccrea@keesaco.com of Keesaco
	def __init__(self, name = None):
		self.group_name = name