###########################################################################
## \file app/DataStructures/PluginReference.py
## \brief Contains the plugin reference class.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################
## \package app.DataStructures.PluginReference
## \brief Provides a reference to a specific plugin.
###########################################################################


## \brief Plugin reference class for holding information about the location of a plugin.
class PluginReference:
	
	###########################################################################
	## \brief Constructor for the PluginReference object.
	## \param self - instance reference
	## \param path - path through which the plugin can be located in the data store
	## \return Returns PluginReference object on success. Returns false on fail.
	## \note Will fail if no path is given.
	## \warning Does not check that the path for the plugin exists.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def __init__(self, path):
		if path == None:
			return False
		## The path at which the plugin can be found.
		self.path = path
		return self

