###########################################################################
## \file app/Permissions/Types.py
## \brief contains classes for permissions, users, groups and for grouping these classes to form permission sets
## \author jmccrea@keesaco.com of Keesaco
###########################################################################
## \package app.Permissions.Types
## \brief Defines classes for storing users, groups and for grouping these classes to form permission sets
###########################################################################

## \brief Group class for holding information about a usergroup
class Group:
	###########################################################################
	## \brief constructor - creates a Group instance with a given groupname
	## \param Group self - instance reference
	## \param String name - (= None) name of user group
	## \return None
	## \author jmccrea@keesaco.com of Keesaco
	###########################################################################
	def __init__(self, name = None):
		## name of the use group
		self.group_name = name

## \brief A group and permission pairing to represent the permissions a group has for a resource
class GroupAccess:

	###########################################################################
	## \brief Constructs a GroupAccess instance for a given Group and Permissions instance
	## \param GroupAccess self - instance reference
	## \param Group group - (= None) the group the permissions belong to
	## \param Permissions permissions - (= None) the permissions the group have
	## \return None
	## \author jmccrea@keesaco.com of Keesaco
	###########################################################################
	def __init__(self, group = None, permissions = None):
		## Group instance - the group the permissions belong to
		self.group = group
		## Permissions instance - the permissions the group have
		self.permissions = permissions

## \brief defines a set of permissions which an entity has to a resource
class Permissions:

	###########################################################################
	## \brief Constructs a Permissions instance with given permissions
	## \param Permissions self - intance reference
	## \param Boolean read - (= False) read access
	## \param Boolean write - (= False) write access
	## \param Boolean full_control - (= False) full control
	## \return None
	## \note if full_control is true, read and write will also be forced true
	## \author jmccrea@keesaco.com of Keesaco
	###########################################################################
	def __init__(self, read = False, write = False, full_control = False):
		#Initialise all to false
		
		## read access
		self.read = False
		## write access
		self.write = False
		## full control
		self.full_control = False
		
		self.set_permissions(read, write, full_control)
	
	###########################################################################
	## \brief sets the permissions to a given set of permissions
	## \param Permissions self - intance reference
	## \param Boolean read - (= False) set read access
	## \param Boolean write - (= False) set write access
	## \param Boolean full_control - (= False) [Boolean] full control
	## \return None
	## \note if full_control is True, read and write will also be forced True
	## \author jmccrea@keesaco.com of Keesaco
	###########################################################################
	def set_permissions(self, read = False, write = False, full_control = False):
		self.full_control = full_control
		if full_control:
			self.read = True
			self.write = True
		else:
			self.read = read
			self.write = write

## \brief Defines a set of users and groups and their permissions to access a resource as well as the currently authenticated user
class PermissionSet:

	###########################################################################
	## \brief Constructs a PermissionSet instance for a given authenticated user
	## \param PermissionSet self - instance reference
	## \param User authed_user - (= None) the currently authenticated user, usually this user's permissions will be checked when attempting to access resources
	## \return None
	## \author jmccrea@keesaco.com of Keesaco
	###########################################################################
	def __init__(self, authed_user = None):
		## The currently authenticated user
		self.authed_user = authed_user
		## List of UserAccess objects to define permissions belonging to users
		self.users = []
		## List of GroupAccess objects to define permissions belonging to groups
		self.groups = []
	
	###########################################################################
	## \brief Adds a user/permissions pair to the list of users/permissions
	## \param PermissionSet self - instance reference
	## \param UserAccess new_user - UserAccess object representing the user and permissions pairing to be added to the user list
	## \return None
	## \author jmccrea@keesaco.com of Keesaco
	###########################################################################
	def add_user(self, new_user):
		self.users.append(new_user)
	
	###########################################################################
	## \brief Adds a group/permissions pair to the list of groups/permissions
	## \param PermissionSet self - instance reference
	## \param GroupAccess new_group - GroupAccess object representing the group and permissions pairing to be added to the group list
	## \return none
	## \author jmccrea@keesaco.com of Keesaco
	###########################################################################
	def add_group(self, new_group):
		self.groups.append(new_group)

## \brief Contains information about a user
class User:

	###########################################################################
	## \brief Constructs a User object with a given name
	## \param User self - instance reference
	## \param String name - (= None) username of created user
	## \return None
	## \author jmccrea@keesaco.com of Keesaco
	###########################################################################
	def __init__(self, name = None):
		##User's username
		self.username = name


## \brief A user and permissions pair to represent the access permissions a user has for a resource
class UserAccess:

	###########################################################################
	## \brief Constructs a UserAccess instance for given User and Permissions instances
	## \param UserAccess self - instance reference
	## \param User user - (= None) the user which the permissions belong to
	## \param Permissions permissions - (= None) permissions which the user has
	## \return None
	## \author jmccrea@keesaco.com of Keesaco
	###########################################################################
	def __init__(self, user = None, permissions = None):
		## User instance - the user to define permissions for
		self.user = user
		## Permissions instnace - the permissions the user has
		self.permissions = permissions