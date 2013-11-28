## \file shared/python/structures/data_ref.py
# \brief Contains the data reference class
# \author swhitehouse@keesaco.com of Keesaco

## \brief Data reference class for holding information about a portion of a data set.
class Group:
	
	## \brief Constructor for the data_ref object.
	# \param self - instance reference
	# \param path - path through which the data can be located in the data store
	# \param start - (= 0) the start point of the data to be included in analysis
	# \param end - (= 0) the end point of the data to be included in analysis
	# \return Returns data_ref object on success. Returns false on fail.
	# \note Will fail if no path is given.
	# \note Will fail if end is less than start.
	# \note Setting both start and end to 0 (as is default) will include all of the available data in analysis.
	# \warning Does not check that the path for the data exists.
	# \author swhitehouse@keesaco.com of Keesaco
	def __init__(self, path, start = 0, end = 0):
		self.path = path
		self.start_set = start
		self.end_set = end

