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
## \brief gets user details from the permissions DB
## \param user_id - [String] unique ID of user to look up
## \return	None if not found or User object
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
## \note Looks up user details in DB then tries to find more details using Google services, if the user's details have changed since last login this will not be possible and last-known details form the DB will be used as a fall-back
## \todo check and update user details if found using Google auth
###########################################################################
def get_user_by_id(user_id):
	users = Users.query(Users.unique_id == user_id)
	user = users.get()
	
	if user is None:
		## user not found
		return None
	else:
		user_obj = User(user.email_address)
		
		## return user object if details were retrieved from Google
		if user_obj.found:
			return user_obj
		else:
			## set unknown details from records
			user_obj.set_unque_id(user.user_id)
			user_obj.set_nickname(user.nickname)
			return user_obj



###########################################################################
## \brief gets a user's details from the key of entry in the Users table
## \param user_key - [Key] the key to look up
## \return User object or None if not found
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
## \todo Stub - This shares logic with get_user_by_id - consider reviewing/abstracting this, also see todo on get_user_by_id
###########################################################################
def get_user_by_key(user_key):
	user = user_key.get()

	if user is None:
		## user not found
		return None
	else:
		user_obj = User(user.email_address)

		## return user object if details were retrieved from Google
		if user_obj.found:
			return user_obj
		else:
			## set unknown details from records
			user_obj.set_unque_id(user.user_id)
			user_obj.set_nickname(user.nickname)
			return user_obj



###########################################################################
## \brief Add a file to the file table with a given name and owner
## \param new_file_name - [String] name of file to add
## \param new_file_owner_key - [Key] key of user which owns the new file
## \return key of new file
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
## \todo Currently this does not check if the file exists or if there is already an entry for it - consider reviewing this and implementing some checking
###########################################################################
def add_file(new_file_name, new_file_owner_key):
	new_file = Files(	parent = ndb.Key("FileTable", "*notitle*"),
					 	file_name = new_file_name,
					 	owner_key = new_file_owner_key );
						
	return new_file.put();

###########################################################################
## \brief
## \param
## \return
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
## \todo Stub - needs implementing
###########################################################################
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
def add_file_permissions(file_key, permissions):
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
