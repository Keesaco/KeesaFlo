

class FileStat:
	
	def __init__(	self,
					filename,
					st_size,
					etag,
					st_ctime,
					content_type=None,
					metadata=None,
					is_dir=False)):
	
		self.filename = filename
		self.is_dir	= is_dir
		self.st_size = st_size
		self.etag = etag
		self.st_ctime = st_ctime
		self.content_type = content_type
		self.metadata = metadata