###########################################################################
## \file app/API/PALDatastore.py
## \brief Containts the PALDatastore package: Platform Abstraction Layer for data access
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
## \package app.API.PALDatastore
## \brief Contains abstraction layer functions for 'low level' data access - returns results in a platform independent form
## \note Depends on FileStat and cloudstorage (google)
###########################################################################
#import sys
#sys.path.append("/home/rogan/Coursework/SPE/Keesaco/app/googleAPI/cloudstorageAPI/src/cloudstorage")
import cloudstorage as gcs
from FileStat import FileStat

##directory seperator
DIRECTORY_SEPARATOR = '/'

###########################################################################
## \brief Opens a resource for write/read/edit etc.
## \param file_name - name of file to open
## \param mode - (= 'r') mode to open file in
## \param MIME_type - (= None) MIME type of data to access
## \param options - (= None)
## \param read_buff_size - (= storage_api.ReadBuffer.DEFAULT_BUFFER_SIZE) size of read buffer (max = 30MB)
## \param retry_params - (= None)
## \return file handle for opened file or None on failure
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def open(	file_name,
			mode = 'r',
			MIME_type = None,
			options = None,
			read_buff_size = gcs.storage_api.ReadBuffer.DEFAULT_BUFFER_SIZE,
			retry_params = None	):
	try:
		file_handle = gcs.open( file_name, mode, MIME_type, options, read_buff_size, retry_params)
	
	except gcs.NotFoundError:
		return None
	else:
		return file_handle
	
	
###########################################################################
## \brief Deletes a resource
## \param file_name - name of resource to delete
## \param retry_params - (= None)
## \return boolean (true = success, false otherwise)
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def delete(	file_name,
			retry_params = None	):
	try:
		gcs.delete(file_name, retry_params)
	except gcs.NotFoundError:
		return False
	else:
		return True

		
		
###########################################################################
## \brief Transfers the data of a google provided GCSFileStat object into a FileStat object
## \param gcs_file_stat - the GCSFileStat object to transfer data from
## \return FileStat object - the genericised FileStat object
## \author cwike@keesaco.com of Keesaco
###########################################################################
def __gcs_file_stat_conversion__( gcs_file_stat ):
	file_stat = FileStat(	gcs_file_stat.filename,
							gcs_file_stat.st_size,
							gcs_file_stat.etag,
							gcs_file_stat.st_ctime,
							gcs_file_stat.content_type,
							gcs_file_stat.metadata,
							gcs_file_stat.is_dir)
	return file_stat
	
###########################################################################
## \brief Gets information about a specified resource
## \param file_name - name of resource to get information about
## \param retry_params - (= None)
## \return FileStat object - object containing information about specified resource, None on failure
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def stat(	file_name,
			retry_params = None	):
	try:
		gcs_stat = gcs.stat( file_name )
		
	except gcs.NotFoundError:
		return None
	except gcs.AuthorizationError:
		return None
	else:
		file_stat = __gcs_file_stat_conversion__( gcs_stat )
		return file_stat
	
###########################################################################
## \brief Lists the contents of a storage bucket
## \param path - path of bucket to list (string)
## \param marker - (= None) further path, only resources following this marker will be listed
## \param prefix - (= None) DEPRECATED (Use path prefix)
## \param max_keys - (= None) limits the number of resources listed (None = no limit)
## \param delimiter - (= None) used to turn on directory mode (string of one or multiple characters used as a directory seperator)
## \param retry_params - (= None)
## \return list of FileStat objects
## \author jmccrea@keesaco.com of Keesaco
## \author cwike@keesaco.com of Keesaco
###########################################################################
def list_bucket(	path,
					marker = None,
					prefix = None, #deprecated
					max_keys = None,
					delimiter = None,
					retry_params = None	):
	file_stat_list =[]
	gcs_stat_iterator = gcs.listbucket( path, marker, prefix, max_keys, delimiter, retry_params)
	
	for gcs_stat in gcs_stat_iterator:
		file_stat_list.append(__gcs_file_stat_conversion__( gcs_stat ))
		
	return file_stat_list