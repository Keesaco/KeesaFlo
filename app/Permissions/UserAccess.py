## \file app/permissions/UserAccess.py
# \brief Contains the UserAccess class for user/permissions pairs
# \author jmccrea@keesaco.com of Keesaco

from User import *
from Permissions import *

## \brief A user and permissions pair to represent the access permissions a user has for a resource
class UserAccess:
	## User instance - the user to define permissions for
	user = User()
	## Permissions instnace - the permissions the user has
	permissions = Permissions()
	
	## \brief Constructs a UserAccess instance for given User and Permissions instances
	# \param self - instance reference
	# \param user - (= None) [User] the user which the permissions belong to
	# \param permissions - (= None) [Permissions] permissions which the user has
	# \return UserAccess instance for the given user and permissions
	# \author jmccrea@keesaco.com of Keesaco
	def __init__(self, user = None, permissions = None):
		self.user = user
		self.permissions = permissions