## \file shared/python/permissions/User.py
# \brief Contains the User class
# \author jmccrea@keesaco.com of Keesaco

## \brief Contains information about a user
class User:
	
	##User's username
	username = ""

	## \brief Constructs a User object with a given name
	# \param self - instance reference
	# \param name - (= None) [String] username of created user
	# \return User instance
	# \author jmccrea@keesaco.com of Keesaco
	def __init__(self, name = None):
		self.username = name
	