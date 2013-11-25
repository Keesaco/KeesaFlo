## \file shared/python/permissions/GroupAccess.py
# \brief Contains the GroupAccess class for group/permissions pairs
# \author jmccrea@keesaco.com of Keesaco

from Group import *
from Permissions import *

## \brief A group and permission pairing to represent the permissions a group has for a resource
class GroupAccess:
	
	## Group instance - the group the permissions belong to
	group = None
	## Permissions instance - the permissions the group have
	permissions = None
	
	## \brief Constructs a GroupAccess instance for a given Group and Permissions instance
	# \param self - instance reference
	# \param group - (= None) [Group] the group the permissions belong to
	# \param permissions - (= None) [Permissions] the permissions the group have
	# \return GroupAccess instance for given Group and Permissions
	# \author jmccrea@keesaco.com of Keesaco
	def __init__(self, group = None, permissions = None):
		self.group = group
		self.permissions = permissions