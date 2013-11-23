from UserAccess import *
from GroupAccess import *
from User import *

class PermissionsObject:
	
	authedUser = User()
	users = []
	groups = []
	
	def __init__(self):
		pass