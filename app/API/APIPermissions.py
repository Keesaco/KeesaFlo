
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
## \brief 	Add a file to the file table with a given name and owner
## \param	FileInfo new_file - the file to be added to the datastore
## \param	Bool return_updated -  (= False) if true the return value the
##			original file with its key property updated
## \return 	If return_updated is true the returns the original file
##			argument with an updated key property. Otherwise returns the
##			key of the new Files entry as it was inserted.
## \author 	jmccrea@keesaco.com of Keesaco
## \author 	cwike@keesaco.com of Keesaco
## \todo 	Currently this does not check if the file exists or if there is
##			already an entry for it - consider reviewing this and
##			implementing some checking
###########################################################################
def add_file(new_file, return_updated = False):
	return PAL.add_file(new_file, return_updated)

###########################################################################
## \brief Removes a file object from the Files table
## \param file_key - [Key] key of file object
## \return true on aparrent success, false otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def remove_file_by_key(file_key):
	if PAL.revoke_all_by_file_key(file_key):
		return PAL.remove_file_by_key(file_key)

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
	return PAL.rename_file_by_key(file_key, new_file_name)

###########################################################################
## \brief 	Updates a file using a given FileInfo object.
##			To locate the entry to update, the key property of the given
##			FileInfo object is checked. If one is not found, the file_name
##			property will be used instead.
## \param 	FileInfo new_file - updated file information to be stored
## \return 	True on aparrent success, False otherwise
## \author 	jmccrea@keesaco.com of Keesaco
###########################################################################
def update_file(new_file):
	return PAL.update_file(new_file)

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
## \param String new_color - the user-defined colour tag for the file
## \param Bool new_starred - whether or not the user has starred the file
## \return entity key
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def add_file_permissions(permissions_file_key,permissions_user_key, permissions, new_colour = '000000', new_starred = False):
	return PAL.add_file_permissions(permissions_file_key, permissions_user_key, permissions, new_colour, new_starred)

###########################################################################
## \brief modifies permissions on permissions entry 
## \param permissions key - [Key] key of permissions entry
## \param new_permissions - [Permissions] new permissions to set
## \param Bool new_starred - (= None) new starred value for entry
## \param String new_colour - (= None) new colour for file
## \return True on success, False otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def modify_file_permissions_by_key(permissions_key, new_permissions = None, new_starred = None, new_colour = None):
	return PAL.modify_file_permissions_by_key(permissions_key,new_permissions, new_starred, new_colour)

###########################################################################
## \brief modifies permissions on permissions entry
## \param file_key - [Key] key of file entry permissions pertain to
## \param user_key - [Key] key of user entry permissions pertain to
## \param permissions - [Permissions] new permissions to set
## \param Bool new_starred - (= None) new starred value for entry
## \param String new_colour - (= None) new colour for file
## \return  True on success, False otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def modify_file_permissions_by_keys(file_key, user_key, permissions = None, new_starred = None, new_colour = None):
	return PAL.modify_file_permissions_by_keys(file_key,user_key, permissions, new_starred, new_colour)

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
## \return FilePermissions object on sucess, None otherwise
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

###########################################################################
## \brief adds a named element to element table
## \param ref - [String] reference to named element
## \return key of new entry
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def add_element(ref):
	return PAL.add_element(ref)

###########################################################################
## \brief removes a named element from table by name
## \param element_ref - [String] name of named element
## \return True on success, False otherwise
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def remove_element_by_ref(element_ref):
	return PAL.remove_element_by_ref(element_ref)

###########################################################################
## \brief removes a named element from table by entry key
## \param element_key - [Key] key of entry to remove
## \return True on success, False otherwise
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def remove_element_by_key(element_key):
	return PAL.remove_element_by_key(element_key)

###########################################################################
## \brief renames element reference
## \param old_ref - [String] named reference to rename
## \param new_ref - [String] new name for element
## \return key of element renamed
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def rename_element(old_ref, new_ref):
	return PAL.rename_element(old_ref, new_ref)

###########################################################################
## \brief gets an element by key
## \param element_key - [Key] key of element to get
## \return element os success or None
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def get_element_by_key(element_key):
	return PAL.get_element_by_key(element_key)

###########################################################################
## \brief gets element key by element reference
## \param element_ref - [String] named element reference
## \return key of element on success, None otherwise
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def get_element_key_by_ref(element_ref):
	return PAL.get_element_key_by_ref(element_ref)

###########################################################################
## \brief adds an element permissions entry
## \param u_key - [Key] user key of entry
## \param e_key - [Key] element key of entry
## \param set_access - [Boolean] permissions
## \return key of new object
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def add_element_permissions(u_key,e_key,set_access):
	return PAL.add_element_permissions(u_key,e_key,set_access)

###########################################################################
## \brief modifies an element permission by key
## \param key - [Key] key of entry
## \param new_access - [Boolean] new access 
## \return key of object ot false on failure
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def modify_element_permissions_by_key(key,new_access):
	return PAL.modify_element_permissions_by_key(key,new_access)

###########################################################################
## \brief modifies an element permission by keys
## \param user_key - [Key] key of user
## \param element_key - [Key] key of element
## \param new_access - [Boolean] new access perameter
## \return key or False on failure
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def modify_user_element_permissions(user_key,element_key,new_access):
	return PAL.modify_user_element_permissions(user_key,element_key,new_access)

###########################################################################
## \brief revokes all permissions in an element
## \param element_key - [Key] key of element to be revoked by
## \return True on success, False otherwise
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def revoke_element_permissions_element_key(element_key):
	return PAL.revoke_element_permissions_element_key(element_key)

###########################################################################
## \brief revokes all permisions by user
## \param user_key - [Key] user to revoke on
## \return True on success, False otherwise
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def revoke_element_permissions_user_key(user_key):
	return PAL.revoke_element_permissions_user_key(user_key)

###########################################################################
## \brief revokes a permission based on user and element
## \param user_key - [Key] key of user to revoke by
## \param element_key - [Key] key of element to revoke by
## \return True on success, False otherwise
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def revoke_user_element_permissions(user_key,element_key):
	return PAL.revoke_user_element_permissions(user_key,element_key)

###########################################################################
## \brief revoke a permission entry by its key
## \param key - [Key] key to revoke by
## \return True on success, False otherwise
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def revoke_element_permissions_by_key(key):
	return PAL.revoke_element_permissions_by_key(key)

###########################################################################
## \brief gets all perfmissions attached to an element
## \param element_key - [Key] key of element to get by
## \return iterator over all permissions attached to element
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def get_element_permissions_by_element_key(element_key):
	return PAL.get_element_permissions_by_element_key(element_key)

###########################################################################
## \brief gets all perfmissions attached to an user
## \param user_key - [Key] key of user to get by
## \return iterator over all permissions attached to user
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def get_element_permissions_by_user_key(user_key):
	return PAL.get_element_permissions_by_user_key(user_key)

###########################################################################
## \brief gets permission attached to user and element
## \param user_key - [Key] key of user to get by
## \param element_key - [Key] key of user to get by
## \return object on success, None otherwise 
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def get_user_element_permissions(user_key,element_key):
	return PAL.get_user_element_permissions(user_key,element_key)

###########################################################################
## \brief gets an element permissions by key
## \param key - [Key] key of pernissions to get
## \return object or None
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def get_element_permissions_by_key(key):
	return PAL.get_element_permissions_by_key(key)

###########################################################################
## \brief gets a key of permissions by keys
## \param user_key - [Key] user entry pertains to
## \param element_key - [Key] element entry pertains to
## \return key on success, False otherwise
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def get_user_element_permissions_key(user_key, element_key):
	return PAL.get_user_element_permissions_key(user_key, element_key)
