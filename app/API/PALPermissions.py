###########################################################################
## \file app/API/PALPermissions.py
## \brief Containts the PALDatastore package: Platform Abstraction Layer for permission data access
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
## \package app.API.PALPermissions
## \brief Contains abstraction layer functions for platform-specific permission table functionality. Results are returned to a calling API in a plaform-independent format
###########################################################################

from API.PALDBTables import Users, Files, FilePermissions
from API.User import User
from google.appengine.ext import ndb


###########################################################################
## \brief Adds a new user entry to the Users table
## \param user - [User] user object for the user to be added to the table
## \return key of newly added user
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def add_user(user):
	new_user = Users(	parent = ndb.Key("UserTable", "*notitle*"),
					 	unique_id = user.user_id(),
					 	nickname = user.nickname(),
					 	email_address = user.email()		)
	return new_user.put();

###########################################################################
## \brief
## \param
## \return
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
## \todo Stub - needs implementing
###########################################################################
def remove_user_by_id(user_id):
	pass

###########################################################################
## \brief
## \param
## \return
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
## \todo Stub - needs implementing
###########################################################################
def modify_user_by_id(user_id, new_user):
	pass

###########################################################################
## \brief
## \param
## \return
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
## \todo Stub - needs implementing
###########################################################################
def get_user_by_id(user_id):
	pass

###########################################################################
## \brief
## \param
## \return
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
## \todo Stub - needs implementing
###########################################################################
def get_user_by_key(user_key):
	pass

###########################################################################
## \brief
## \param
## \return
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
## \todo Stub - needs implementing
###########################################################################
def add_file(file_name, owner_key):
	pass

def remove_file_by_key(file_key):
	pass

###########################################################################
## \brief
## \param
## \return
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
## \todo Stub - needs implementing
###########################################################################
def rename_file_by_key(file_key, new_file_name):
	pass

###########################################################################
## \brief
## \param
## \return
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
## \todo Stub - needs implementing
###########################################################################
def get_file_by_key(file_key):
	pass

###########################################################################
## \brief
## \param
## \return
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
## \todo Stub - needs implementing
###########################################################################
def get_file_by_name(file_name):
	pass

###########################################################################
## \brief
## \param
## \return
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
## \todo Stub - needs implementing
###########################################################################
def add_file_permissions(file_key, permissions)
	pass

###########################################################################
## \brief
## \param
## \return
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
## \todo Stub - needs implementing
###########################################################################
def modify_file_permissions_by_key(permissions_key, permissions):
	pass

###########################################################################
## \brief
## \param
## \return
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
## \todo Stub - needs implementing
###########################################################################
def modify_file_permissions_by_keys(file_key, user_key, permissions):
	pass

###########################################################################
## \brief
## \param
## \return
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
## \todo Stub - needs implementing
###########################################################################
def revoke_all_by_file_key(file_key):
	pass

###########################################################################
## \brief
## \param
## \return
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
## \todo Stub - needs implementing
###########################################################################
def revoke_all_by_user_key(user_key):
	pass

###########################################################################
## \brief
## \param
## \return
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
## \todo Stub - needs implementing
###########################################################################
def revoke_permissions_by_key(permissions_key):
	pass

###########################################################################
## \brief
## \param
## \return
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
## \todo Stub - needs implementing
###########################################################################
def revoke_user_file_permissions(file_key, user_key):
	pass

###########################################################################
## \brief
## \param
## \return
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
## \todo Stub - needs implementing
###########################################################################
def get_user_file_permissions(file_key, user_key):
	pass

###########################################################################
## \brief
## \param
## \return
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
## \todo Stub - needs implementing
###########################################################################
def get_file_permissions_list(file_key):
	pass

###########################################################################
## \brief
## \param
## \return
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
## \todo Stub - needs implementing
###########################################################################
def get_user_permissions_list(user_key):
	pass