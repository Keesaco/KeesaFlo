from UserAccess import *
from GroupAccess import *
from User import *

class PermissionsObject:
	
	authedUser = User()
	users = []
	groups = []
	
	def __init__(self, authedUser = None):
		self.authedUser = authedUser

	def addUser(self, newUser):
		self.users.append(newUser)

	def addGroup(self, newGroup):
		self.groups.append(newGroup)
