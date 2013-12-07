###########################################################################
## \file app/Analysis/Types/ExtTypes.py
## \brief Contains all analysis types.
## \author swhitehouse@keesaco.com of Keesaco
###########################################################################
## \package app.Analysis.Types.ExtTypes
## \brief Provides all external type classes associated with analysis.
###########################################################################


## \brief Data reference class for holding information about a portion of a data set.
class DataReference:

	###########################################################################
	## \brief Constructor for the DataReference object.
	## \param self - instance reference
	## \param path - path through which the data can be located in the data store
	## \param set - (= [(0, 0)]) a list of the start and end points (in bytes) of the subsets of data to be analysed
	## \return Returns DataReference object on success. Returns false on fail.
	## \note Will fail if no path is given.
	## \note Will fail if first value in the tuple is greater than the second.
	## \note Leaving set as default will include all of the available data in analysis.
	## \warning Does not check that the path for the data exists.
	## \author swhitehouse@keesaco.com of Keesaco
	###########################################################################
	def __init__(	self,
					path,
					set = [(0, 0)]	):
		if path == None:
			return False
		for (x, y) in set:
			if x > y:
				return False
		## The path at which the data can be found.
		self.path = path
		## The subset of data being referenced.
		self.subset = set
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

