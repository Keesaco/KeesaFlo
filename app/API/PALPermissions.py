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

def add_user(user):
	new_user = Users(	parent = ndb.Key("UserTable", "*notitle*"),
					 	unique_id = user.user_id(),
					 	nickname = user.nickname(),
					 	email_address = user.email()		)
	new_user.put();
	