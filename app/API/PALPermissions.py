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
## \brief Removes a user entry from the database given that use's unique ID
## \param user_id - [String] unique ID of user to remove
## \return True on success, False on failure
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
## \note The return value is not affected by the return value of the actual deletion as the actual ndb.Key.delete method always returns None
###########################################################################
def remove_user_by_id(user_id):
	users = Users.query(Users.unique_id == user_id)
	user = users.get()
	
	if user is None:
		return False
	else:
		user.key.delete()
		return True

###########################################################################
## \brief Removes a user from the database given the key of the user entry
## \param user_key - [Key] key of user entry to remove
## \return True on success, False on error
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
## \note The return value is not affected by the return value of the actual deletion as the actual ndb.Key.delete method always returns None
###########################################################################
def remove_user_by_key(user_key):
	#Check that given key is actually a Key object
	if isinstance(user_key, ndb.Key):
		user_key.delete()
		return True
	else:
		#Can't remove due to invalid key, return False
		return False



###########################################################################
## \brief update a user's details in the database given the user's ID
## \param user_id - [String] ID of user to update
## \param new_user - [String]
## \return
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def modify_user_by_id(user_id, new_user):
	users = Users.query(Users.unique_id == user_id)
	user = users.get()

	if user is None:
		return False
	else:
		user.user_id 	= new_user.user_id()
		user.nickname 	= new_user.nickname()
		user.email 		= new_user.email()

		return user.put()

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
			user_obj.set_user_id(user.user_id)
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
	if isinstance(user_key, ndb.Key):
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
	else:
		return False



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
## \brief Removes a file object from the Files table
## \param file_key - [Key] key of file object
## \return true on aparrent success, false otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
## \todo Stub - needs testing
###########################################################################
def remove_file_by_key(file_key):
	if isinstance(file_key,ndb.Key):
		file_key.delete()
		return True
	else:
		return False

###########################################################################
## \brief Renames a file stored in a Files object, via Files table key lookup
## \param file_key - [Key] key of file object
## \param new_file_name - [String] new name to call file
## \return true on aparrent success, false otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
## \todo Stub - needs testing
###########################################################################
def rename_file_by_key(file_key, new_file_name):
	if isinstance(file_key,ndb.Key):
		file = file_key.get()
		file.file_name = new_file_name
		file.put()
		return True
	else:
		return False

###########################################################################
## \brief gets a file object from its key
## \param file_key - [Key] key of file object
## \return returns file object on success or None
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
## \todo Stub - needs testing
###########################################################################
def get_file_by_key(file_key):
	if isinstance(file_key,ndb.Key):
		file = file_key.get()
		return file
	else:
		return None
		

###########################################################################
## \brief gets a file object from its internal file name
## \param file_name - [String] name of file stored in file object
## \return returns first matching file object on success or None
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
## \todo Stub - needs testing
###########################################################################
def get_file_by_name(file_name):
	query = Files.query(Files.file_name == file_name)
	file = query.get()
	return file
	
###########################################################################
## \brief gets list of files by owner key
## \param owner_key - [Key] owner key of file
## \return returns iterator object over Files objects
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
## \todo Stub - needs testing
###########################################################################
def get_file_by_owner_key(owner_key):
	if isinstance(owner_key,ndb.Key):
		query = Files.query(Files.owner_key == owner_key)
		iterator = query.iter()
		return iterator
	else:
		return None
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

	
	
		
		
		
		
