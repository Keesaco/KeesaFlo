## \file shared/python/permissions/Permissions.py
# \brief Contains the Permissions class for storing a set of permissions one entity has to a resource
# \author jmccrea@keesaco.com of Keesaco

class Permissions:
	## read access
	read = False
	## write access
	write = False
	## full control
	full_control = False
	
	## \brief Constructs a Permissions instance with given permissions
	# \param self - intance reference
	# \param read - (= False) [Boolean] read access
	# \param write - (= False) [Boolean] write access
	# \param full_control - (= False) [Boolean] full control
	# \return A Permissions instance with the given permissions
	# \note if full_control is true, read and write will also be forced true
	# \author jmccrea@keesaco.com of Keesaco
	def __init__(self, read = False, write = False, full_control = False):
		self.setPermissions(read, write, fullControl)

	## \brief sets the permissions to a given set of permissions
	# \param self - intance reference
	# \param read - (= False) [Boolean] set read access
	# \param write - (= False) [Boolean] set write access
	# \param full_control - (= False) [Boolean] full control
	# \return none
	# \note if full_control is True, read and write will also be forced True
	# \author jmccrea@keesaco.com of Keesaco
	def setPermissions(self, read = False, write = False, full_control = False):
		self.full_control = full_control
		if full_control:
			self.read = True
			self.write = True
		else:
			self.read = read
			self.write = write


		
