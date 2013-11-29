###########################################################################
## \file app/API/FileStat.py
## \brief contains the FileStat class
## \author cwike@keesaco.com of Keesaco
###########################################################################

## \brief contains statistics about a file in the datastore
class FileStat:

	###########################################################################
	## \brief constructor for a FileStat object
	## \param self - instance reference
	## \param filename - path\filename of file
	## \param st_size - file size in bytes
	## \param etag	- MD5 hex digest of file
	## \param st_ctime - posix file creation time
	## \param content_type - MIMEtype of file
	## \param metadata - metadata of file
	## \param is_dir - boolean. True if directory, False if file
	## \return returns a FileStat object
	## \author cwike@keesaco.com of keesaco
	###########################################################################
	def __init__(	self,
					filename,
					st_size = None,
					etag = None,
					st_ctime = None,
					content_type=None,
					metadata=None,
					is_dir=False):
	
		self.filename = filename
		self.is_dir	= is_dir
		self.st_size = st_size
		self.etag = etag
		self.st_ctime = st_ctime
		self.content_type = content_type
		self.metadata = metadata