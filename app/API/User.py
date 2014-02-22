###########################################################################
## \file app/API/User.py
## \brief contains the User class
## \author cwike@keesaco.com of Keesaco
###########################################################################
## \package app.API.User
## \brief Defines class for holding information about users
###########################################################################

from google.appengine.api import users


## \brief contains User class hold information about a user
class User:

	###########################################################################
	## \brief constructor for a User object
	## \param self - instance reference
	## \param email_addr - email address of user, or None for current user
	## \param federated_identity - openId identifier, or None
	## \return returns a User object
	## \author cwike@keesaco.com of keesaco
	###########################################################################
	def __init__(self,
				 email_addr = None,
				 federated_identity = None
				):
				
		self._federated_ident = None
		self._nickname = None
		self._user_id = None
		self._federated_provider = None
		self._email = None
		self.found = False
		
		try:
			google_user = users.User(email_addr,federated_identity)
		except users.UserNotFoundError:
			pass
		else:
			self._federated_ident = google_user.federated_identity()
			self._nickname = google_user.nickname()
			self._user_id = google_user.user_id()
			self._federated_provider = google_user.federated_provider()
			self._email = google_user.email()
			self.found = True

	###########################################################################
	## \brief getter for nickname
	## \return returns a string of nickname
	## \author cwike@keesaco.com of keesaco
	###########################################################################
	def nickname(self):
		return self._nickname
	
	
	###########################################################################
	## \brief getter for email
	## \return returns a string of email
	## \author cwike@keesaco.com of keesaco
	###########################################################################
	def email(self):
		return self._email
	
	
	###########################################################################
	## \brief getter for user id
	## \return returns a string of user_id
	## \author cwike@keesaco.com of keesaco
	###########################################################################
	def user_id(self):
		return self._user_id
	
	
	###########################################################################
	## \brief getter for federated_identity
	## \return returns a string of openID federated identity
	## \author cwike@keesaco.com of keesaco
	###########################################################################
	def federated_identity(self):
		return self._federated_ident
	
	
	###########################################################################
	## \brief getter for federated_provider
	## \return returns a string of openID federated provider
	## \author cwike@keesaco.com of keesaco
	###########################################################################
	def federated_provider(self):
		return self._federated_provider

	###########################################################################
	## \brief setter for user nickname
	## \param nickname - [String] new nickname
	## \return None
	## \author cwike@keesaco.com of keesaco
	## \author jmccrea@keesaco.com of keesaco
	###########################################################################
	def set_nickname(self, nickname):
		self._nickname = nickname

	###########################################################################
	## \brief setter for unique_id
	## \param unique_id - [String] new unique_id
	## \return None
	## \author cwike@keesaco.com of keesaco
	## \author jmccrea@keesaco.com of keesaco
	###########################################################################
	def set_unique_id(self, unique_id):
		self._unique_id = unique_id


