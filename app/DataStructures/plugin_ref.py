## \file app/DataStructures/plugin_ref.py
# \brief Contains the plugin reference class.
# \author swhitehouse@keesaco.com of Keesaco

## \brief Plugin reference class for holding information about the location of a plugin.
class plugin_ref:
	
	## \brief Constructor for the plugin_ref object.
	# \param self - instance reference
	# \param path - path through which the plugin can be located in the data store
	# \return Returns plugin_ref object on success. Returns false on fail.
	# \note Will fail if no path is given.
	# \warning Does not check that the path for the plugin exists.
	# \author swhitehouse@keesaco.com of Keesaco
	def __init__(self, path):
		if path == None:
			return False
		## The path at which the plugin can be found.
		self.path = path
		return self

