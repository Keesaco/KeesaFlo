###########################################################################
## \file app/API/PALPermissions.py
## \brief Containts the PALDatastore package: Platform Abstraction Layer for permission data access
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
## \package app.API.PALPermissions
## \brief Contains abstraction layer functions for platform-specific permission table functionality. Results are returned to a calling API in a plaform-independent format
###########################################################################

from API.PALDBTables import Users, Files, FilePermissions, Elements, ElementPermissions
from API.User import User
from google.appengine.ext import ndb
from Permissions.Types import FileInfo

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
	new_file = Files(	parent = ndb.Key("FileTable", "*notitle*"),
					 	file_name = new_file.file_name,
					 	owner_key = new_file.owner_key,
					 	friendly_name = new_file.friendly_name,
					 	prev_file_key = new_file.prev_file_key)
	new_key = new_file.put();

	if return_updated:
		new_file.key = new_key
	else:
		return new_key

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
## \note This action can be performed using update_file
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
## \brief 	Updates a file using a given FileInfo object.
##			To locate the entry to update, the key property of the given
##			FileInfo object is checked. If one is not found, the file_name
##			property will be used instead.
## \param 	FileInfo new_file - updated file information to be stored
## \return 	True on aparrent success, False otherwise
## \author 	jmccrea@keesaco.com of Keesaco
###########################################################################
def update_file(new_file):
	if isinstance(new_file.key ,ndb.Key):
		file = new_file.key.get()
	else:
		file = get_file_by_name(new_file.file_name)

	if file is None:
		return False
	else:
		file.file_name 		= new_file.file_name
		file.owner_key		= new_file.owner_key
		file.friendly_name 	= new_file.friendly_name
		file.put()
		return True

###########################################################################
## \brief gets a file object from its key
## \param file_key - [Key] key of file object
## \return returns file object on success or None
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def get_file_by_key(file_key):
	if isinstance(file_key,ndb.Key):
		file = file_key.get()

		if file is None:
			return None
		else:
			return FileInfo(	file_name 		= file.file_name,
								owner_key 		= file.owner_key,
								friendly_name 	= file.friendly_name,
								key				= file.key)
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
	file = query.get()
	
	if file is None:
		return None
	else:
		return FileInfo(	file_name 		= file.file_name,
							owner_key 		= file.owner_key,
							friendly_name 	= file.friendly_name,
							key				= file.key)

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
## \param String new_color - the user-defined colour tag for the file
## \param Bool new_starred - whether or not the user has starred the file
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
## \param Bool new_starred - (= None) new starred value for entry
## \param String new_colour - (= None) new colour for file
## \return True on success, False otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def modify_file_permissions_by_key(permissions_key, new_permissions = None, new_starred = None, new_colour = None):
	if isinstance(permissions_key,ndb.Key):

		permissions = permissions_key.get()
		if new_permissions is not None:
			permissions.read = new_permissions.read
			permissions.write = new_permissions.write
			permissions.full_control = new_permissions.full_control
		
		if new_starred is not None:
			permissions.starred = new_starred
			
		if new_colour is not None:
			permissions.colour = new_colour
		
		permissions.put()
		
		return True
	else:
		return False

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
def modify_file_permissions_by_keys(file_key, user_key, new_permissions = None, new_starred = None, new_colour = None):
	if (isinstance(user_key,ndb.Key)) and (isinstance(file_key,ndb.Key)):
		query = FilePermissions.query(ndb.AND(FilePermissions.user_key == user_key,
											 FilePermissions.file_key == file_key))

		permissions = query.get()
		if new_permissions is not None:
			permissions.read = new_permissions.read
			permissions.write = new_permissions.write
			permissions.full_control = new_permissions.full_control

		if new_starred is not None:
			permissions.starred = new_starred

		if new_colour is not None:
			permissions.colour = new_colour

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
## \return FilePermissions object on sucess, None otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def get_user_file_permissions(file_key, user_key):
	if (isinstance(user_key,ndb.Key)) and (isinstance(file_key,ndb.Key)):
		query = FilePermissions.query(ndb.AND(FilePermissions.user_key == user_key,
											 FilePermissions.file_key == file_key))
		return query.get()
	else:
		return None

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
		return None


###########################################################################
## \brief adds a named element to element table
## \param ref - [String] reference to named element
## \return key of new entry
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def add_element(ref):
	elem = Elements(element_ref = ref)
	return elem.put()

###########################################################################
## \brief removes a named element from table by name
## \param element_ref - [String] name of named element
## \return True on success, False otherwise
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def remove_element_by_ref(element_ref):
	query = Elements.query(Elements.element_ref == element_ref)
	elem = query.get()

	if elem is None:
		return False
	else:
		elem.key.delete()
		return True

###########################################################################
## \brief removes a named element from table by entry key
## \param element_key - [Key] key of entry to remove
## \return True on success, False otherwise
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def remove_element_by_key(element_key):
	if isinstance(element_key,ndb.Key):
		element_key.delete()
		return True
	else:
		return False

###########################################################################
## \brief renames element reference
## \param old_ref - [String] named reference to rename
## \param new_ref - [String] new name for element
## \return key of element renamed
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def rename_element(old_ref, new_ref):
	query = Elements.query(Elements.element_ref == old_ref)
	elem = query.get()

	elem.element_ref = new_ref
	return elem.put()

###########################################################################
## \brief gets an element by key
## \param element_key - [Key] key of element to get
## \return element os success or None
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def get_element_by_key(element_key):
	if isinstance(element_key,ndb.Key):
		element = element_key.get()
		return element
	else:
		return None

###########################################################################
## \brief gets element key by element reference
## \param element_ref - [String] named element reference
## \return key of element on success, None otherwise
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def get_element_key_by_ref(element_ref):
	query = Elements.query(Elements.element_ref == element_ref)
	elem = query.get()
	if elem is None:
		return None
	else:
		return elem.key

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
	obj = ElementPermissions(	user_key = u_key,
								element_key = e_key,
								access = set_access )

	return obj.put()
###########################################################################
## \brief modifies an element permission by key
## \param key - [Key] key of entry
## \param new_access - [Boolean] new access 
## \return key of object or None on failure
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def modify_element_permissions_by_key(key,new_access):
	obj = key.get()

	if obj is not None:
		obj.access = new_access
		return obj.put()
	return None

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
	if (isinstance(user_key,ndb.Key)) and (isinstance(element_key,ndb.Key)):
		query = ElementPermissions.query(ndb.AND(ElementPermissions.user_key == user_key,
											 ElementPermissions.element_key == element_key))

		obj = query.get()
		if obj is not None:
			obj.access = new_access
			return obj.put
	return None

###########################################################################
## \brief revokes all permissions in an element
## \param element_key - [Key] key of element to be revoked by
## \return True on success, False otherwise
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def revoke_element_permissions_element_key(element_key):
	if(isinstance(element_key,ndb.Key)):
		query = ElementPermissions.query(ElementPermissions.element_key == element_key)
		iterator = query.iter()
		for entry in iterator:
			entry.key.delete()
		return True
	else:
		return False

###########################################################################
## \brief revokes all permisions by user
## \param user_key - [Key] user to revoke on
## \return True on success, False otherwise
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def revoke_element_permissions_user_key(user_key):
	if(isinstance(user_key,ndb.Key)):
		query = ElementPermissions.query(ElementPermissions.user_key == user_key)
		iterator = query.iter()
		for entry in iterator:
			entry.key.delete()
		return True
	else:
		return False

###########################################################################
## \brief revokes a permission based on user and element
## \param user_key - [Key] key of user to revoke by
## \param element_key - [Key] key of element to revoke by
## \return True on success, False otherwise
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def revoke_user_element_permissions(user_key,element_key):
	if (isinstance(user_key,ndb.Key)) and (isinstance(element_key,ndb.Key)):
		query = ElementPermissions.query(ndb.AND(ElementPermissions.user_key == user_key,
											 ElementPermissions.element_key == element_key))
		query.get().key.delete()
		return True
	else:
		return False

###########################################################################
## \brief revoke a permission entry by its key
## \param key - [Key] key to revoke by
## \return True on success, False otherwise
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def revoke_element_permissions_by_key(key):
	if isinstance(key,ndb.Key):
		key.delete()
		return True
	else:
		return False

###########################################################################
## \brief gets all perfmissions attached to an element
## \param element_key - [Key] key of element to get by
## \return iterator over all permissions attached to element
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def get_element_permissions_by_element_key(element_key):
	if(isinstance(element_key,ndb.Key)):
		query = ElementPermissions.query(ElementPermissions.element_key == element_key)
		return query.iter()
	else:
		return None

###########################################################################
## \brief gets all perfmissions attached to an user
## \param user_key - [Key] key of user to get by
## \return iterator over all permissions attached to user
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def get_element_permissions_by_user_key(user_key):
	if(isinstance(user_key,ndb.Key)):
		query = ElementPermissions.query(ElementPermissions.user_key == user_key)
		return query.iter()
	else:
		return None

###########################################################################
## \brief gets permission attached to user and element
## \param user_key - [Key] key of user to get by
## \param element_key - [Key] key of user to get by
## \return object on success, None otherwise 
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def get_user_element_permissions(user_key,element_key):
	if (isinstance(user_key,ndb.Key)) and (isinstance(element_key,ndb.Key)):
		query = ElementPermissions.query(ndb.AND(ElementPermissions.user_key == user_key,
											 ElementPermissions.element_key == element_key))
		return query.get()
	else:
		return None

###########################################################################
## \brief gets an element permissions by key
## \param key - [Key] key of pernissions to get
## \return object or None
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def get_element_permissions_by_key(key):
	if isinstance(key,ndb.Key):
		return key.get()
	else:
		return None

###########################################################################
## \brief gets a key of permissions by keys
## \param user_key - [Key] user entry pertains to
## \param element_key - [Key] element entry pertains to
## \return key on success, False otherwise
## \author cwike@keesaco.com of Keesaco
## \note Untested - Needs testing
###########################################################################
def get_user_element_permissions_key(user_key, element_key):
	if (isinstance(user_key,ndb.Key)) and (isinstance(element_key,ndb.Key)):
		query = ElementPermissions.query(ndb.AND(ElementPermissions.user_key == user_key,
											 ElementPermissions.element_key == element_key))
		return query.get().key
	else:
		return None
