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
	user_id 		= ndb.KeyProperty()
	### - file ID
	file_id 		= ndb.KeyProperty()

	###Permissions
	### - read access
	read 			= ndb.BooleanProperty()
	### - write access
	write 			= ndb.BooleanProperty()
	### - full control
	full_control 	= ndb.BooleanProperty()