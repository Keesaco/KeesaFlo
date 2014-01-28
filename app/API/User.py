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
	## \param email - email address of user, or None for current user
	## \param federated_identity - openId identifier, or None
	## \return returns a User object
	## \author cwike@keesaco.com of keesaco
	###########################################################################
	def __init__(self,
				 email = None,
				 federated_identity = None
				):
		try:
			user = users.User(email,federated_identity)
		except users.UserNotFoundError:
			self.email = None
			self.nickname = None
			self.user_id = None
			self.federated_provider = None
			self.email = None
			
		else:
			self.federated_identity = user.federated_identity()
			self.nickname = user.nickname()
			self.user_id = user.user_id()
			self.federated_provider = user.federated_provider()
			self.email = user.email()	

	###########################################################################
	## \brief getter for nickname
	## \return returns a string of nickname
	## \author cwike@keesaco.com of keesaco
	###########################################################################
	def nickname(self):
		return self.nickname
	
	
	###########################################################################
	## \brief getter for email
	## \return returns a string of email
	## \author cwike@keesaco.com of keesaco
	###########################################################################
	def email(self):
		return self.email
	
	
	###########################################################################
	## \brief getter for user id
	## \return returns a string of user_id
	## \author cwike@keesaco.com of keesaco
	###########################################################################
	def user_id(self):
		return self.user_id
	
	
	###########################################################################
	## \brief getter for federated_identity
	## \return returns a string of openID federated identity
	## \author cwike@keesaco.com of keesaco
	###########################################################################
	def federated_identity(self):
		return self.federated_identity
	
	
	###########################################################################
	## \brief getter for federated_provider
	## \return returns a string of openID federated provider
	## \author cwike@keesaco.com of keesaco
	###########################################################################
	def federated_provider(self):
		return self.federated_provider
		
		
		