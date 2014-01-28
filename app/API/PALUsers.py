###########################################################################
## \file app/API/PALUsers.py
## \brief Containts the PALUsers package: Platform Abstraction Layer for user authentication
## \author cwike@keesaco.com of Keesaco
###########################################################################
## \package app.API.PALUsers
## \brief Contains abstraction layer functions for user authentication functions
## \note Depends on google.appengine.api.users (google)
###########################################################################

from google.appengine.api import users
from User import User

###########################################################################
## \brief Creates a url that points to a login page
## \param dest_url - url to redirect to after login
## \param federated_identity - openId identifier
## \return url to login page or None on failure
## \author cwike@keesaco.com of Keesaco
###########################################################################
def create_login_url(dest_url=None, federated_identity=None):
	try:
		url = users.create_login_url(dest_url,federated_identity)
	except users.NotAllowedError:
		return None
	else:
		return url

###########################################################################
## \brief Creates a url that points to a logout page
## \param dest_url - url to redirect to after logout
## \return url to logout page
## \author cwike@keesaco.com of Keesaco
###########################################################################
def create_logout_url(dest_url):
	return users.create_logout_url(dest_url)

###########################################################################
## \brief gets the current authenticated user
## \return User object or None
## \author cwike@keesaco.com of Keesaco
###########################################################################
def get_current_user():
	return users.get_current_user()

###########################################################################
## \brief determines if current user is on admins list
## \return true if admin, false otherwise
## \author cwike@keesaco.com of Keesaco
###########################################################################
def is_current_user_admin():
	if users.is_current_user_admin():
		return True
	else:
		return False
