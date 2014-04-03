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
from Permissions import Types

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
		user.unique_id 	= new_user.user_id()
		user.nickname 	= new_user.nickname()
		user.email_address		= new_user.email()

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
## \brief gets user details from the permissions DB
## \param user_id - [String] unique ID of user to look up
## \return	None if not found or User key
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def get_user_key_by_id(user_id):
	users = Users.query(Users.unique_id == user_id)
	user = users.get()
	
	if user is None:
		## user not found
		return None
	else:
		return user.key


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
def add_file(new_file_name, new_file_owner_key, new_friendly_name = ""):
	new_file = Files(	parent = ndb.Key("FileTable", "*notitle*"),
					 	file_name = new_file_name,
					 	owner_key = new_file_owner_key,
					 	friendly_name = new_friendly_name);
						
	return new_file.put();

###########################################################################
## \brief Removes a file object from the Files table
## \param file_key - [Key] key of file object
## \return true on aparrent success, false otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
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
###########################################################################
def get_file_by_key(file_key):
	if isinstance(file_key,ndb.Key):
		files = file_key.get()
		return files
	else:
		return None
		

###########################################################################
## \brief gets a file object from its internal file name
## \param file_name - [String] name of file stored in file object
## \return returns first matching file object on success or None
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def get_file_by_name(file_name):
	query = Files.query(Files.file_name == file_name)
	files = query.get()
	return files
	
###########################################################################
## \brief gets list of files by owner key
## \param owner_key - [Key] owner key of file
## \return returns iterator object over Files objects
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def get_file_by_owner_key(owner_key):
	if isinstance(owner_key,ndb.Key):
		query = Files.query(Files.owner_key == owner_key)
		iterator = query.iter()
		return iterator
	else:
		return None
###########################################################################
## \brief adds file permissions entry to file permissions table
## \param permissions_file_key - [Key] key of file to set permissions
## \param permissions_user_key - [Key] key of user to assign file permissions to
## \param permissions - [Permissions] permissions object setting permissions
## \return entity key
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def add_file_permissions(permissions_file_key,permissions_user_key, permissions, new_colour = '000000', new_starred = False):
	new_permission = FilePermissions( 	parent = ndb.Key("PermissionsTable", "*notitle*"),
										user_key = permissions_user_key,
										file_key = permissions_file_key,
										read = permissions.read,
										write = permissions.write,
										full_control = permissions.full_control,
									 	colour = new_colour,
									 	starred = new_starred );
	return new_permission.put()

###########################################################################
## \brief modifies permissions on permissions entry 
## \param permissions key - [Key] key of permissions entry
## \param new_permissions - [Permissions] new permissions to set
## \return True on success, False otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def modify_file_permissions_by_key(permissions_key, new_permissions):
	if isinstance(permissions_key,ndb.Key):
		permissions = permissions_key.get()
		permissions.read = new_permissions.read
		permissions.write = new_permissions.write
		permissions.full_control = new_permissions.full_control
		permissions.put()
		return True
	else:
		return False

###########################################################################
## \brief modifies permissions on permissions entry
## \param file_key - [Key] key of file entry permissions pertain to
## \param user_key - [Key] key of user entry permissions pertain to
## \param permissions - [Permissions] new permissions to set
## \return  True on success, False otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def modify_file_permissions_by_keys(file_key, user_key, new_permissions):
	if (isinstance(user_key,ndb.Key)) and (isinstance(file_key,ndb.Key)):
		query = FilePermissions.query(ndb.AND(FilePermissions.user_key == user_key,
											 FilePermissions.file_key == file_key))

		permissions = query.get()
		permissions.read = new_permissions.read
		permissions.write = new_permissions.write
		permissions.full_control = new_permissions.full_control
		permissions.put()
		return True
	else:
		return False

###########################################################################
## \brief removes all file permissions entries pertaining to file entry
## \param file_key - [Key] key of file entry a permissions entry references
## \return True on success, False otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def revoke_all_by_file_key(file_key):
	if(isinstance(file_key,ndb.Key)):
		query = FilePermissions.query(FilePermissions.file_key == file_key)
		iterator = query.iter()
		for entry in iterator:
			entry.key.delete()
		return True
	else:
		return False

###########################################################################
## \brief removes all file permissions pertaining to an user entry
## \param user_key - [Key] key of user entry a permissions entry references
## \return True on success, False otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def revoke_all_by_user_key(user_key):
	if(isinstance(user_key,ndb.Key)):
		query = FilePermissions.query(FilePermissions.user_key == user_key)
		iterator = query.iter()
		for entry in iterator:
			entry.key.delete()
		return True
	else:
		return False

###########################################################################
## \brief removes a file permission
## \param permissions_key - [Key] key of permissions entry
## \return True on success, False otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def revoke_permissions_by_key(permissions_key):
	if isinstance(permissions_key,ndb.Key):
		permissions_key.delete()
		return True
	else:
		return False

###########################################################################
## \brief removes a file permissions
## \param file_key - [Key] key of file entry pertains to
## \param user_key - [Key] key of user entry pertains to
## \return True on success, False otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def revoke_user_file_permissions(file_key, user_key):
	if (isinstance(user_key,ndb.Key)) and (isinstance(file_key,ndb.Key)):
		query = FilePermissions.query(ndb.AND(FilePermissions.user_key == user_key,
											 FilePermissions.file_key == file_key))
		query.get().key.delete()
		return True
	else:
		return False

###########################################################################
## \brief retrieves a entry from the permissions table
## \param file_key - [Key] key of file entry pertains to
## \param user_key - [Key] key of user entry pertains to
## \return FilePermissions object on sucess, False otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def get_user_file_permissions(file_key, user_key):
	if (isinstance(user_key,ndb.Key)) and (isinstance(file_key,ndb.Key)):
		query = FilePermissions.query(ndb.AND(FilePermissions.user_key == user_key,
											 FilePermissions.file_key == file_key))
		return query.get()
	else:
		return False

###########################################################################
## \brief retrieves a entry from the permissions table
## \param permissions_key - [Key] key of permissions entry pertains to
## \return FilePermissions object on sucess, False otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def get_permissions_by_key(permissions_key):
	if isinstance(permissions_key,ndb.Key):
		permissions = permissions_key.get()
		return permissions
	else:
		return None

###########################################################################
## \brief gets a list of permissions pertaining to a file
## \param file_key - [Key] key of file entries pertain to
## \return iterator object over FilePermissions object on sucess, or False otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def get_file_permissions_list(file_key):
	if(isinstance(file_key,ndb.Key)):
		query = FilePermissions.query(FilePermissions.file_key == file_key)
		return query.iter()
	else:
		return False

###########################################################################
## \brief gets a list of permissions pertaining to a user
## \param user_key - [Key] key of user entries pertain to
## \return iterator object over FilePermissions object on sucess, or False otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def get_user_permissions_list(user_key):
	if(isinstance(user_key,ndb.Key)):
		query = FilePermissions.query(FilePermissions.user_key == user_key)
		return query.iter()
	else:
		return False
