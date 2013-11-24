
# This is a comment
class Permissions:
	read = False
	write = False
	fullControl = False
	
	def __init__(self, read = False, write = False, fullControl = False):
		self.setPermissions(read, write, fullControl)

	def setPermissions(self, read = False, write = False, fullControl = False):
		self.read = read
		self.write = write
		self.fullControl = fullControl


		