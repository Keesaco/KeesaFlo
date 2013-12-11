###########################################################################
## \file app/API/APIDatastore.py
## \brief Defines the datastore API for data access. Built upon PALDatastore for cross-platform support.
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
## \package app.API.APIDatastore
## \brief Provides methods for data access, using PALDatastore for platform independence
## \note Depends on PALDatastore
###########################################################################

import PALDatastore

## \brief second tier API for data access - utilises PAL for low level file access

###########################################################################
## \brief Checks the authentication of the user against the file
## \param path - filepath of data to check
## \param action - intended action on data
## \param permissions - user attempting to perform access
## \return returns True if authourised else False
## \todo Stub: returns True, needs implementing
## \author cwike@keesaco.com of Keesaco
###########################################################################
def __check_authentication (	path,
							action ='r', #d = delete
								permissions = None):
	return True

###########################################################################
## \brief Checks the existance of file or directory being searched
## \param path - path of file to check
## \param permissions - the user to check authed
## \return if exists, as far as the user is aware,return True, else False
## \author cwike@keesaco.com of Keesaco
###########################################################################	
def check_exists (	path,
					permissions):
	if __check_authentication ( path, 'r' , permissions ):
		if PALDatastore.stat( path ) is None :
			return False
		else:
			return True
	else:
		return False

###########################################################################
## \brief Gets the path of the containing directory of the passed file/directory
## \param path - [String] path of file/directory to find parent of
## \return path to containing directory
## \warning This method does not check that the file/directory passed in exists or that the current user has permissions to access it. It merely performs string manipulations.
## \author jmccrea@keesaco.com of Keesaco
###########################################################################
def get_container(	path	):
	bucket = path.lstrip('/').partition(PALDatastore.DIRECTORY_SEPARATOR) #gets bucket name
	rpart = bucket[2].rpartition(PALDatastore.DIRECTORY_SEPARATOR)
	if len(rpart[2]) == 0: #directory
		rpart = rpart[0].rpartition(PALDatastore.DIRECTORY_SEPARATOR)
	return "/"+bucket[0]+bucket[1]+rpart[0]+rpart[1]
							 
###########################################################################
## \brief Creates a new file and optionally opens it in a given mode
## \param path - path of file to create
## \param blob - binary object to write into file on creation
## \param mode - (= None) mode to open file in (None = file not opened)
## \param permssions - (= None) permissions object for current user and permissions to apply to file
## \return on success returns file handle for created file or True if mode = None, on failure returns False
## \note this method will fail if the directory does not already exist
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def add_file(	path,
				blob = None,
				mode = None,
				permissions = None ):
	if check_exists( path, permissions ):
		return False
	else:
		file_handle = PALDatastore.open(path,'w')
		if file_handle is None:
			return False
		if blob is not None:
			file_handle.write(blob)
		file_handle.close()
		add_permissions( path, permissions, True)
		if mode is None:
			return False
		else:
			return PALDatastore.open(path, mode)

###########################################################################	
## \brief Generates a path from information about a file
## \param inner_path - path within directory to access
## \param data_type - type of data to access (directory depends on this)
## \param file_name - (= "") name of file within directory to access
## \return returns a path within the correct directory for the specified data type
## \warning This method only returns a path, it does not check that the path exists or check the permissions on that path
## \note generate_path( "somepath/", someType, "somefile.ext" ) is functionally identical to generate_path( "somepath/somefile.ext", someType )
## \todo stub - needs implementing
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def generate_path(	inner_path,
					data_type,
					file_name = ""	):
	
	return inner_path + file_name #Simply return the path and filename for now

###########################################################################
## \brief Appends a blob to an existing file
## \param path - path to file to append to
## \param blob - binary object to append to specified file
## \param permssions - (= None) permissions object for current user
## \return True on success, false otherwise
## \todo Make it work
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def append(	path,
			blob,
			permissions = None	):
	if __check_authentication( path, 'a', permissions):
		if check_exists( path, permissions ):
			file_handle = PALDatastore.open( path, 'a')
			file_handle.write(blob)
			return True
		else:
			return False
	else:
		return False

###########################################################################
## \brief Opens a file for reading/editing
## \param path - path of file to open
## \param mode - (= 'r') mode to open file in
## \param permssions - (= None) permissions object for current user
## \return returns file handle on success or False on failure
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def open(	path,
			mode = 'r',
			permissions = None):
	if __check_authentication( path, mode, permissions):
		if check_exists( path, permissions):
			return PALDatastore.open( path, mode )

	return False

###########################################################################
## \brief Closes an open file
## \param file_handle - handle for file to close
## \return True on success, False otherwie
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def close(	file_handle	):
	file_handle.close()

###########################################################################
## \brief Creates a new directory
## \param path - path of directory to create
## \warning path requires a trailing slash currently.
## \param permssions - (= None) permissions object for current user and permissions to apply to new directory
## \return True on success, False otherwise
## \todo Make it work in root
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def add_directory(	path,
					permissions = None	):
	if check_exists(path, permissions):
		return False
	else:
		if check_exists(get_container(path),permissions):
			file_handle = PALDatastore.open(path, 'w')
			if file_handle is None:
				return False
			else:
				file_handle.close();
				return True
		else:
			return False


###########################################################################
## \brief Lists the contents of a directory
## \param path - path of directory to list
## \param permssions - (= None) permissions object for current use
## \return list of FileInfo objects for files/directories in the specified directory, False on failure
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def list(	path,
			permissions = None ):
	
	if __check_authentication(path, 'r', permissions): #check permissions to read directory
		return PALDatastore.list_bucket(path) #call into PAL to list bucket

	return False #return false on failure

###########################################################################
## \brief Deletes a specified file or directory
## \param path - path to file/directory to remove
## \param permissions - (= None) permissions object for current user
## \param allow_dir - (= False) if false, the method will fail if the specified path refers to a directory
## \return True on success, False otherwise
## \todo implement directory deletion
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def delete( path,
			permissions = None,
			allow_dir = False ):
			
	if allow_dir:
		return False
	else:
		if __check_authentication(path, 'd'):
			return PALDatastore.delete(path)

	return False

###########################################################################
## \brief Moves a specified file/directory to a different location
## \param source - path to file/directory to move
## \param destination - path of directory to move file/directory into
## \param permissions - (= None) permissions object for current user
## \param allow_dir - (= False) if false, the method will fail if the specified source path refers to a directory
## \return True on success, False otherwise
## \todo Stub: not yet implemented
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def move(	source,
			destination,
			permissions = None,
			allow_dir = False ):
	pass

###########################################################################
## \brief Makes a copy of a file or a directory in a different location, optionally with different permissions
## \param source - path to file/directory to copy
## \param destination - destination directory for copy to be made in
## \param permissions - (= None) permissions object for current user
## \param allow_dir - (= False) if false, the method will fail if the specified path refers to a directory
## \param alter_permissions - (= False) if a permissions object is passed, the contained permissions will be applied to the copy
## \return True on success, False otherwise
## \todo Stub: not yet implemented
## \note using alter_permissions will cause the given permissions object to overwrite the old permissions on the copy, but will leave the source file's permissions intact
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def copy(	source,
			destination,
			permissions = None,
			alter_permissions = False,
			allow_dir = False	):
	pass

###########################################################################
## \brief Adds new groups/users to a file/directory with specified permissions
## \param path - path of file/directory to change permissions of
## \param permissions - (= None) permissions object for current user and permissions for new users/groups to be added
## \param allow_dir - (= False) if false, the method will fail if the specified path refers to a directory
## \return True on success, False otherwise
## \note	permissions will only be added, not updated or removed - if a user already has permissions and the permissions object specifies different permissions, that user's permissions will not be updated. Additionally, if a user has permissions and that user is not listed within the permissions object, that user's permissions will not be removed.
## \todo Stub: this should be implemented once the permissionsntable has been implemented/specified
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def	add_permissions(	path,
						permissions,
						allow_dir = False	):
	return True

###########################################################################
## \brief Edits the permissions on a file or directory
## \param path - path to file/directory to update permissions of
## \param permissions - (= None) permissions object for current user and users/groups to update
## \param allow_dir - (= False) if false, the method will fail if the specified path refers to a directory
## \note	edit_permissions will only update permissions, i.e. it will not remove a user/groups's permissions if they already have access but are not listed in the permissions object. It will also not add a user/group if they appear in the permissions object but do not have existing permissions for the file/directory
## \return True on success, False otherwise
## \todo Stub: this should be implemented once the permissionsntable has been implemented/specified
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def edit_permissions(	path,
						permissions,
						overwrite = False,
						allow_dir = False	):
	return True

###########################################################################
## \brief Removes users'/groups' permissions from a specified file/directory
## \param path - path to file/directory to delete permissions from
## \param permissions - (= None) permissions object for current user and lists of users/groups whose permissions are to be removed
## \param allow_dir - (= False) if false, the method will fail if the specified path refers to a directory
## \note delete_permissions will always delete a user's/group's permissions if they are listed in the permissions object, even if the permissions specified in the permissions object differ from their current permissions on the file itself.
## \return True on success, False otherwise
## \todo Stub: this should be implemented once the permissionsntable has been implemented/specified
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def delete_permissions(	path,
						permissions = None,
						allow_dir = False	 ):
	return True

###########################################################################
## \brief Overwrites users'/groups' permissions for a specified file/directory
## \param path - path to file/directory to overwrite permissions for
## \param permissions - these permissions will replace the existing permissions on the specified file/directory
## \param allow_dir - (= False) if false, the method will fail if the specified path refers to a directory
## \return True on success, False otherwise
## \todo Stub: this should be implemented once the permissionsntable has been implemented/specified
## \author jmccrea@keesaco.com of Keesaco
###########################################################################
def overwrite_permissions(	path,
						  	permissions,
						  	allow_dir = False	):
	return True

###########################################################################
## \brief Gets a permissions object representing a file's permissions
## \param path - path to list permissions for
## \param permissions - (= None) permissions object for current user
## \param allow_dir - (= False) if false, the method will fail if the specified path refers to a directory
## \return Permissions objects representing users and groups and their respective permissions
## \todo Stub: this should be implemented once the permissionsntable has been implemented/specified
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def get_permissions(	path,
						permissions = None,
						allow_dir = False	):
	return None
