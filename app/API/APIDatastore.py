###########################################################################
## \file app/API/APIDatastore.py
## \brief defines the datastore API for data access. Built upon PALDatastore for cross-platform support.
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################

import PALDatastore

## \brief second tier API for data access - utilises PAL for low level file access

###########################################################################
## __check_authentication - checks the authentication of the user against the file
## \param path - filepath of data to check
## \param action - intended action on data
## \param user - user attempting to perform access
## \return returns True if authourised else False
## \todo Stub: returns True, needs implementing
## \author cwike@keesaco.com of Keesaco
###########################################################################
def __check_authentication (	path,
								action ='r',
								user = None):
	return True

###########################################################################
## check_exists - checks the existance of file or directory being searched
## \param path - path of file to check
## \param authed_user - the user to check authed
## \return if exists, as far as the user is aware,return True, else False
## \todo test functionality
## \author cwike@keesaco.com of Keesaco
###########################################################################	
def check_exists (	path,
					authed_user):
	if __check_authentication ( path, 'r' , authed_user ):
		if PALDatastore.stat( path ) == None :
			return False
		else:
			return True
	else:
		return False
		
###########################################################################
## add_file - creates a new file and optionally opens it in a given mode
## \param path - path of file to create
## \param blob - binary object to write into file on creation
## \param mode - (= None) mode to open file in (None = file not opened)
## \param permssions - (= None) permissions object for current user and permissions to apply to file
## \return on success returns file handle for created file or True if mode = None, on failure returns False
## \note this method will fail if the directory does not already exist
## \todo test functionality
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def add_file(	path,
				blob = None,
				mode = None,
				permissions = None ):
	if check_exists( path, permissions.authed_user):
		return False
	else:
		file_handle = PALDatastore.open(path,'w')
		if file_handle == None
			return False
		if blob != None:
			file_handle.write(blob)
		file_handle.close()
		add_permissions( path, permissions, True)
		if mode == None:
			return False
		else:
			return PALDatastore.open(path, mode)

###########################################################################	
## generate_path - generates a path
## \param inner_path - path within directory to access
## \param data_type - type of data to access (directory depends on this)
## \param file_name - (= "") name of file within directory to access
## \return returns a path within the correct directory for the specified data type
## \warning This method only returns a path, it does not check that the path exists or check the permissions on that path
## \note generate_path( "somepath/", someType, "somefile.ext" ) is functionally identical to generate_path( "somepath/somefile.ext", someType )
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def generate_path(	inner_path,
					data_type,
					file_name = ""	):
	pass

###########################################################################	
## append - appends a blob to an existing file
## \param path - path to file to append to
## \param blob - binary object to append to specified file
## \param permssions - (= None) permissions object for current user
## \return True on success, false otherwise
## \todo test operation
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def append(	path,
			blob,
			permissions = None	):
	if __check_authentication( path, 'a', permissions.authed_user):
		if check_exists( path, permissions.authed_user ):
			file_handle = PALDatastore.open( path, 'a')
			file_handle.write(blob)
			return True
		else:
			return False
	else:
		return False

###########################################################################
## open - opens a file for reading/editing
## \param path - path of file to open
## \param mode - (= 'r') mode to open file in
## \param permssions - (= None) permissions object for current user
## \return returns file handle on success or False on failure
## \todo test operation
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def open(	path,
			mode = 'r',
			permissions = None):
	if __check_authentication( path, mode, permissions.authed_user):
		if check_exists( path, permissions.authed_user):
			return PALDatastore.open( path, mode )
		else:
			return False
	else:
		return False

###########################################################################
## close - closes an open file
## \param file_handle - handle for file to close
## \return True on success, False otherwie
## \todo test operation
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def close(	file_handle	):
	file_handle.close()

###########################################################################
## add_directory - creates a new directory
## \param path - path of directory to create
## \param permssions - (= None) permissions object for current user and permissions to apply to new directory
## \return True on success, False otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def add_directory(	path,
					permissions = None	):
	pass

###########################################################################
## list - lists the contents of a directory
## \param path - path of directory to list
## \param permssions - (= None) permissions object for current use
## \return list of FileInfo objects for files/directories in the specified directory, False on failure
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def list(	path,
			permissions = None ):
	pass

###########################################################################
## delete - deletes a specified file or directory
## \param path - path to file/directory to remove
## \param permissions - (= None) permissions object for current user
## \param allow_dir - (= False) if false, the method will fail if the specified path refers to a directory
## \return True on success, False otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def delete( path,
			permissions = None,
			allow_dir = False ):
	pass

###########################################################################
## move - moves a specified file/directory to a different location
## \param source - path to file/directory to move
## \param destination - path of directory to move file/directory into
## \param permissions - (= None) permissions object for current user
## \param allow_dir - (= False) if false, the method will fail if the specified source path refers to a directory
## \return True on success, False otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def move(	source,
			destination,
			permissions = None,
			allow_dir = False ):
	pass

###########################################################################
## copy - makes a copy of a file or a directory in a different location, optionally with different permissions
## \param source - path to file/directory to copy
## \param destination - destination directory for copy to be made in
## \param permissions - (= None) permissions object for current user
## \param allow_dir - (= False) if false, the method will fail if the specified path refers to a directory
## \param alter_permissions - (= False) if a permissions object is passed, the contained permissions will be applied to the copy
## \return True on success, False otherwise
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
## add_permissions - adds new groups/users to a file/directory with specified permissions
## \param path - path of file/directory to change permissions of
## \param permissions - (= None) permissions object for current user and permissions for new users/groups to be added
## \param allow_dir - (= False) if false, the method will fail if the specified path refers to a directory
## \return True on success, False otherwise
## \note	permissions will only be added, not updated or removed - if a user already has permissions and the permissions object specifies different permissions, that user's permissions will not be updated. Additionally, if a user has permissions and that user is not listed within the permissions object, that user's permissions will not be removed.
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def	add_permissions(	path,
						permissions,
						allow_dir = False	):
	pass

###########################################################################
## edit_permissions - edits the permissions on a file or directory
## \param path - path to file/directory to update permissions of
## \param permissions - (= None) permissions object for current user and users/groups to update
## \param allow_dir - (= False) if false, the method will fail if the specified path refers to a directory
## \note	edit_permissions will only update permissions, i.e. it will not remove a user/groups's permissions if they already have access but are not listed in the permissions object. It will also not add a user/group if they appear in the permissions object but do not have existing permissions for the file/directory
## \return True on success, False otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def edit_permissions(	path,
						permissions,
						overwrite = False,
						allow_dir = False	):
	pass

###########################################################################
## delete_permissions - removes users'/groups' permissions from a specified file/directory
## \param path - path to file/directory to delete permissions from
## \param permissions - (= None) permissions object for current user and lists of users/groups whose permissions are to be removed
## \param allow_dir - (= False) if false, the method will fail if the specified path refers to a directory
## \note delete_permissions will always delete a user's/group's permissions if they are listed in the permissions object, even if the permissions specified in the permissions object differ from their current permissions on the file itself.
## \return True on success, False otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def delete_permissions(	path,
						permissions = None,
						allow_dir = False	 ):
	pass

###########################################################################
## get_permissions - gets a permissions object representing a file's permissions
## \param path - path to list permissions for
## \param permissions - (= None) permissions object for current user
## \param allow_dir - (= False) if false, the method will fail if the specified path refers to a directory
## \return True on success, False otherwise
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def get_permissions(	path,
						permissions = None,
						allow_dir = False	):
	pass
