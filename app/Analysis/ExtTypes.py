###########################################################################
## \file app/Analysis/ExtTypes.py
## \brief Contains all analysis types.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################
## \package app.Analysis.ExtTypes
## \brief Provides all external type classes associated with analysis.
###########################################################################


## \brief Data reference class for holding information about a portion of a data set.
class DataReference:

	###########################################################################
	## \brief Constructor for the DataReference object.
	## \param self - instance reference
	## \param path - path through which the data can be located in the data store
	## \param start - (= 0) the start point of the data to be included in analysis
	## \param end - (= 0) the end point of the data to be included in analysis
	## \return Returns DataReference object on success. Returns false on fail.
	## \note Will fail if no path is given.
	## \note Will fail if end is less than start.
	## \note Setting both start and end to 0 (as is default) will include all of the available data in analysis.
	## \warning Does not check that the path for the data exists.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def __init__(	self,
					path,
					start = 0,
					end = 0	):
		if start > end || start == end != 0 || path == None:
			return False
		## The path at which the data can be found.
		self.path = path
		## The start of the data set to be used (in bytes).
		self.start_set = start
		## The end of the data set to be used (in bytes).
		self.end_set = end
		return self


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
	def __init__(	self,
					path	):
		if path == None:
			return False
		## The path at which the plugin can be found.
		self.path = path
		return self

