################################################################################
## \file 	app/PAL/Files.py
## \brief 	Containts the Files PAL package: Platform Abstraction Layer for file
##			information access.
## \author 	Jack McCrea <contact@jpm.im>
################################################################################
## \package app.PAL.GAE.Files
## \brief 	Contains abstraction layer functions for platform-specific file
##			information functionality. Results are returned to a calling layer
##			in a plaform-independent format. This package should contain only
##			primitive operations - composite operations should be handled by the
##			respective calling API.
################################################################################

from API.PALDBTables import Users, Files, FilePermissions, Elements, ElementPermissions
from google.appengine.ext import ndb
from Permissions.Types import FileInfo

################################################################################
## Read functions
################################################################################

################################################################################
## \brief	Gets a single file by it's name property as used by the file store
## \param	String file_name - name of file to retrieve information for, as used
##				by the file store
## \return	FileInfo instance containing information about the given file on
##				success; None on failure.
## \note	This will only ever return a single object representing a single
##				file, even if multiple entries exist for the same name (which
##				should never happen)
## \todo	Stub; needs implementing
## \author	Jack McCrea <contact@jpm.im>
################################################################################
def get_file_by_name(file_name):
	pass

################################################################################
## \brief	Gets the key of a single file given its name property as used by the
##				file store
## \param	String file_name - name of the file to retrieve the key of, as used
##				by the file store
## \return	FileKey on success, None on failure
## \note	This will only ever return a single result
## \todo	Stub; needs implementing
## \author 	Jack McCrea <contact@jpm.im>
################################################################################
def get_file_key_by_name(file_name):
	pass

################################################################################
## \brief	Gets file information given a file's key
## \param	FileKey file_key - key of the file to get information about
## \return	FileInfo instance on success; None on failure
## \todo	Stub; needs implementing
## \author 	Jack McCrea <contact@jpm.im>
################################################################################
def get_file_from_key(file_key):
	pass

################################################################################
## \brief	Gets the key of a file's immediate parent
## \param	FileKey child_key - key of the child to find the parent of
## \return	FileKey key of the parent file; None on failure or False if the file
##				does not have a parent (i.e. is a root file.)
## \todo	Stub; needs implementing
## \author 	Jack McCrea <contact@jpm.im>
################################################################################
def get_parent_key_from_file_key(child_key):
	pass

################################################################################
## \brief	Gets the keys of a given file's immediate children
## \param	FileKey parent_key - key of the file to find the children of
## \return	FileKey iterator - iterates through keys of all child files. None on
##				failure.
## \todo	Stub; needs implementing
## \author 	Jack McCrea <contact@jpm.im>
################################################################################
def get_child_keys_from_file_key(parent_key):
	pass


################################################################################
## Write functions
################################################################################

################################################################################
## \brief	Stores information about a file
## \param	FileInfo file - the file to store
## \return	FileKey - key the file was inserted with
## \todo	Stub; needs implementing
## \note	Sanity checking - e.g. checking for existing files with the same
##				name - is the responsibility of the API layer.
## \author 	Jack McCrea <contact@jpm.im>
################################################################################
def put_file(file):
	pass

