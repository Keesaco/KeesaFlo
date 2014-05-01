###########################################################################
## \file app/upload_handling.py
## \brief Custom upload handling using our Datastore API. Subclasses Django's FileUploadHandler and UploadedFile.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
## \package app.upload_handling
## \brief Custom upload handling using our Datastore API. Subclasses Django's FileUploadHandler and UploadedFile.
###########################################################################
from django.core.files.uploadhandler import FileUploadHandler
from django.core.files.uploadedfile import UploadedFile
import API.APIDatastore as ds
import API.APIQueue as queue
import API.APIInstance as instances
import API.APIBackground as background
from os.path import splitext
from uuid import uuid1
import buckets

## Custom upload handler class.
class fcsUploadHandler(FileUploadHandler):
	def __init__(self):
		FileUploadHandler.__init__(self)

	###########################################################################
	## \brief Called when a new upload begins. Creates a file in the Datastore and opens it for writing.
	## \param field_name - string name of file <input> field
	## \param file_name - unicode filename provided by browser
	## \param content_type - MIME type provided by browser
	## \param content_length - length of the image provided by the browser (not always provided)
	## \param charset - character set provided by browser (not always provided)
	## \author rmurley@keesaco.com of Keesaco
	###########################################################################
	def new_file(self, field_name, file_name, content_type, content_length, charset):
		## Generate unique datastore path, ensuring uniqueness.
		while True:
			self.name = str(uuid1())
			path = ds.generate_path(bucket.DATA + '/', None, self.name)
			if not ds.check_exists(path, None):
				break
		## Generate friendly name.
		friendly_name = splitext(file_name)[0]
		## Setup file handle.
		self.file_handle = ds.add_file(path, friendly_name, 'raw_data', 'w')
		## Setup uploaded file.
		self.upload = fcsUploadedFile(path, self.name, content_type, charset)
		return None

	###########################################################################
	## \brief Called when the upload handler receives a 'chunk' of data. Writes this chunk to the file opened by new_file and updates md5 hash.
	## \param raw_data - byte string containing the uploaded chunk
	## \param start - position where the raw_data chunk begins
	## \author rmurley@keesaco.com of Keesaco
	###########################################################################
	def receive_data_chunk(self, raw_data, start):
		## Write chunk to datastore.
		self.file_handle.write(raw_data)
		return None

	###########################################################################
	## \brief Called when a file has finished uploading. Closes the Datastore file and starts an analysis task.
	## \param file_size - size of the uploaded file
	## \author rmurley@keesaco.com of Keesaco
	###########################################################################
	def file_complete(self, file_size):
		self.file_handle.close()
		self.upload.size = file_size
		## Start analysis.
		queue.visualise(self.name)
		## Load balance instances in the background.
		background.run(instances.balance, 0)
		return self.upload

## Custom uploaded file class.
class fcsUploadedFile(UploadedFile):
	def __init__(self, path, file_name, content_type, charset):
		UploadedFile.__init__(self)
		self.path = path
		self.name = file_name
		self.content_type = content_type
		self.charset = charset
		self.file_handle = None
		self.mode = None

	###########################################################################
	## \brief Open a datastore file.
	## \param mode - mode to open file in. If mode is none, opens in last used mode.
	## \author rmurley@keesaco.com of Keesaco
	###########################################################################
	def open(self, mode = None):
		if mode is not None:
			self.mode = mode
		self.file_handle = ds.open(self.path, self.mode)
		return self.file_handle

	###########################################################################
	## \brief Read from a datastore file.
	## \param num_bytes - number of bytes to read, if None read whole file
	## \todo Stub: needs implementing
	## \author rmurley@keesaco.com of Keesaco
	###########################################################################
	def read(self, num_bytes = None):
		pass

	###########################################################################
	## \brief Write to a datastore file.
	## \param content - content to write to datastore file
	## \todo Stub: needs implementing
	## \author rmurley@keesaco.com of Keesaco
	###########################################################################
	def write(self, content):
		pass

	###########################################################################
	## \brief Closes a datastore file.
	## \author rmurley@keesaco.com of Keesaco
	###########################################################################
	def close(self):
		ds.close(self.file_handle)
