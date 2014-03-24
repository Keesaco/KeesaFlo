
import PALPermissions as PAL
from API.PALDBTables import Users, Files, FilePermissions
from API.User import User
###########################################################################
## \brief Adds a new user entry to the Users table
## \param user - [User] user object for the user to be added to the table
## \return key of newly added user
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def add_user(user):
	return PAL.add_user(user)

###########################################################################
## \brief Removes a user entry from the database given that use's unique ID
## \param user_id - [String] unique ID of user to remove
## \return True on success, False on failure
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
## \note The return value is not affected by the return value of the actual deletion as the actual ndb.Key.delete method always returns None
###########################################################################
def remove_user_by_id(user_id):
	return PAL.remove_user_by_id(user_id)


###########################################################################
## \brief Removes a user entry from the database given that use's unique ID
## \param user_id - [User] User oject of entry to remove
## \return True on success, False on failure
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
## \note The return value is not affected by the return value of the actual deletion as the actual ndb.Key.delete method always returns None
###########################################################################
def remove_user(user):
	user_id = user.user_id()
	return PAL.remove_user_by_id(user_id)
	
###########################################################################
## \brief Removes a user from the database given the key of the user entry
## \param user_key - [Key] key of user entry to remove
## \return True on success, False on error
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
## \note The return value is not affected by the return value of the actual deletion as the actual ndb.Key.delete method always returns None
###########################################################################
def remove_user_by_key(user_key):
	return PAL.remove_user_by_key(user_key)

###########################################################################
## \brief update a user's details in the database given the user's ID
## \param user_id - [String] ID of user to update
## \param new_user - [String]
## \return
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def modify_user_by_id(user_id, new_user):
	return PAL.modify_user_by_id(user_id, new_user)

###########################################################################
## \brief gets user details from the permissions DB
## \param user_id - [String] unique ID of user to look up
## \return	None if not found or User object
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def get_user_by_id(user_id):
	return PAL.get_user_by_id(user_id)

###########################################################################
## \brief gets user details from the permissions DB
## \param user_id - [String] unique ID of user to look up
## \return	None if not found or key
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def get_user_key_by_id(user_id):
	return PAL.get_user_key_by_id(user_id)

###########################################################################
## \brief gets a user's details from the key of entry in the Users table
## \param user_key - [Key] the key to look up
## \return User object or None if not found
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def get_user_by_key(user_key):
	return PAL.get_user_by_key(user_key)

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
	return PAL.add_file(new_file_name, new_file_owner_key)

###########################################################################
## \brief Removes a file object from the Files table
## \param file_key - [Key] key of file object
## \return true on aparrent success, false otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def remove_file_by_key(file_key):
	return PAL.remove_file_by_key(file_key)

###########################################################################
## \brief Renames a file stored in a Files object, via Files table key lookup
## \param file_key - [Key] key of file object
## \param new_file_name - [String] new name to call file
## \return true on aparrent success, false otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def rename_file_by_key(file_key, new_file_name):
	return PAL.rename_file_by_key(file_key, new_file_name)

###########################################################################
## \brief gets a file object from its key
## \param file_key - [Key] key of file object
## \return returns file object on success or None
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def get_file_by_key(file_key):
	return PAL.get_file_by_key(file_key)

###########################################################################
## \brief gets a file object from its internal file name
## \param file_name - [String] name of file stored in file object
## \return returns first matching file object on success or None
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def get_file_by_name(file_name):
	return PAL.get_file_by_name(file_name)
	
###########################################################################
## \brief gets list of files by owner key
## \param owner_key - [Key] owner key of file
## \return returns iterator object over Files objects
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def get_file_by_owner_key(owner_key):
	return PAL.get_file_by_owner_key(owner_key)

###########################################################################
## \brief adds file permissions entry to file permissions table
## \param permissions_file_key - [Key] key of file to set permissions
## \param permissions_user_key - [Key] key of user to assign file permissions to
## \param permissions - [Permissions] permissions object setting permissions
## \return entity key
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def add_file_permissions(permissions_file_key,permissions_user_key, permissions):
	return PAL.add_file_permissions(permissions_file_key, permissions_user_key, permissions)

###########################################################################
## \brief modifies permissions on permissions entry 
## \param permissions key - [Key] key of permissions entry
## \param new_permissions - [Permissions] new permissions to set
## \return True on success, False otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def modify_file_permissions_by_key(permissions_key, new_permissions):
	return PAL.modify_file_permissions_by_key(permissions_key,new_permissions)

###########################################################################
## \brief modifies permissions on permissions entry
## \param file_key - [Key] key of file entry permissions pertain to
## \param user_key - [Key] key of user entry permissions pertain to
## \param permissions - [Permissions] new permissions to set
## \return  True on success, False otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def modify_file_permissions_by_keys(file_key, user_key, permissions):
	return PAL.modify_file_permissions_by_keys(file_key,user_key, permissions)

###########################################################################
## \brief removes all file permissions entries pertaining to file entry
## \param file_key - [Key] key of file entry a permissions entry references
## \return True on success, False otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def revoke_all_by_file_key(file_key):
	return PAL.revoke_all_by_file_key(file_key)

###########################################################################
## \brief removes all file permissions pertaining to an user entry
## \param user_key - [Key] key of user entry a permissions entry references
## \return True on success, False otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def revoke_all_by_user_key(user_key):
	return PAL.revoke_all_by_user_key(user_key)

###########################################################################
## \brief removes a file permission
## \param permissions_key - [Key] key of permissions entry
## \return True on success, False otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def revoke_permissions_by_key(permissions_key):
	return PAL.revoke_permissions_by_key(permissions_key)

###########################################################################
## \brief removes a file permissions
## \param file_key - [Key] key of file entry pertains to
## \param user_key - [Key] key of user entry pertains to
## \return True on success, False otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def revoke_user_file_permissions(file_key, user_key):
	return PAL.revoke_user_file_permissions(file_key, user_key)

###########################################################################
## \brief retrieves a entry from the permissions table
## \param file_key - [Key] key of file entry pertains to
## \param user_key - [Key] key of user entry pertains to
## \return FilePermissions object on sucess, False otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def get_user_file_permissions(file_key, user_key):
	return PAL.get_user_file_permissions(file_key, user_key)


###########################################################################
## \brief retrieves a entry from the permissions table
## \param permissions_key - [Key] key of permissions entry pertains to
## \return FilePermissions object on sucess, False otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def get_permissions_by_key(permissions_key):
	return PAL.get_permissions_by_key(permissions_key)

###########################################################################
## \brief retrieves a entry from the permissions table
## \param file_key - [Key] key of file entry pertains to
## \param user_key - [Key] key of user entry pertains to
## \return FilePermissions key, False otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def get_user_file_permissions_key(file_key, user_key):
	return PAL.get_user_file_permissions(file_key, user_key).key

###########################################################################
## \brief gets a list of permissions pertaining to a file
## \param file_key - [Key] key of file entries pertain to
## \return iterator object over FilePermissions object on sucess, or False otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def get_file_permissions_list(file_key):
	return PAL.get_file_permissions_list(file_key)

###########################################################################
## \brief gets a list of permissions pertaining to a user
## \param user_key - [Key] key of user entries pertain to
## \return iterator object over FilePermissions object on sucess, or False otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def get_user_permissions_list(user_key):
	return PAL.get_user_permissions_list(user_key)
