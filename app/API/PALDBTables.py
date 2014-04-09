###########################################################################
## \file app/API/PALDBTables.py
## \brief Containts NDB table definitions
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
## \package app.API.PALDBTables
## \brief contains NDB table definitions
###########################################################################

from google.appengine.ext import ndb

class Files(ndb.Model):
	file_name 		= ndb.StringProperty()
	owner_key		= ndb.KeyProperty()


	###	User-set information
	### Allows a (potentially non-unique) name which does not relate to the actual file name
	friendly_name	= ndb.StringProperty()

class Users(ndb.Model):
	### unique ID of user (does not change)
	unique_id 		= ndb.StringProperty()
	### last seen email address of user
	email_address 	= ndb.StringProperty()
	### friendly (display) name for user
	nickname		= ndb.TextProperty()

class FilePermissions(ndb.Model):
	###keys
	### - user ID
	user_key 		= ndb.KeyProperty()
	### - file ID
	file_key 		= ndb.KeyProperty()

	###Permissions
	### - read access
	read 			= ndb.BooleanProperty()
	### - write access
	write 			= ndb.BooleanProperty()
	### - full control
	full_control 	= ndb.BooleanProperty()

	### Not permissions related
	### These properties store user-specific information about a file
	### True if the user has starred the file
	starred 		= ndb.BooleanProperty()
	###	The colour which the user has given to the file
	colour			= ndb.StringProperty()

class Elements(ndb.Model):
	element_ref		= ndb.StringProperty()

class ElementPermissions(ndb.model):
	
	user_key		= ndb.KeyProperty()
	element_key		= ndb.KeyProperty()

	access			= ndb.BooleanProperty()
	
