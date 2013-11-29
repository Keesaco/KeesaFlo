## \file app/permissions/PermissionSet.py
## \brief Contains the PermissionSet class
## \author jmccrea@keesaco.com of Keesaco

from UserAccess import *
from GroupAccess import *
from User import *

## \brief Defines a set of users and groups and their permissions to access a resource as well as the currently authenticated user
class PermissionSet:
	
	## The currently authenticated user
	authedUser = User()
	## List of UserAccess objects to define permissions belonging to users
	users = []
	## List of GroupAccess objects to define permissions belonging to groups
	groups = []
	
	## \brief Constructs a PermissionSet instance for a given authenticated user
	# \param self - instance reference
	# \param authedUser - (= None) [User] the currently authenticated user, usually this user's permissions will be checked when attempting to access resources
	# \return PermissionSet object
	# \author jmccrea@keesaco.com of Keesaco
	def __init__(self, authedUser = None):
		self.authedUser = authedUser

	## \brief Adds a user/permissions pair to the list of users/permissions
	# \param self - instance reference
	# \param newUser - [UserAccess] UserAccess object representing the user and permissions pairing to be added to the user list
	# \return none
	# \author jmccrea@keesaco.com of Keesaco
	def addUser(self, newUser):
		self.users.append(newUser)

	## \brief Adds a group/permissions pair to the list of groups/permissions
	# \param self - instance reference
	# \param newUser - [GroupAccess] GroupAccess object representing the group and permissions pairing to be added to the group list
	# \return none
	# \author jmccrea@keesaco.com of Keesaco
	def addGroup(self, newGroup):
		self.groups.append(newGroup)
