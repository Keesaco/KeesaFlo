## \file app/API/PALDatastore.py
# \brief Containts the PALDatastore class: Platform Abstraction Layer for data access
# \author jmccrea@keesaco.com of Keesaco
# \author cwike@keesaco.com of Keesaco

import cloudstorage as gcs 

## \brief Platoform Abstraction Layer API for 'low level' datastore access


## \brief Constructs a PALDatastore object
# \param self - instance reference
# \return PALDatastore instance
# \author jmccrea@keesaco.com of Keesao
#def __init__(self):
#	pass

## open - opens a resource for write/read/edit etc.
# \param cls - class reference
# \param file_name - name of file to open
# \param mode - (= 'r') mode to open file in
# \param MIME_type - (= None) MIME type of data to access
# \param options - (= None)
# \param read_buff_size - (= storage_api.ReadBuffer.DEFAULT_BUFFER_SIZE) size of read buffer (max = 30MB)
# \param retry_params - (= None)
# \return file handle for opened file or None on failure
# \author jmccrea@keesaco.com of Keesaco
# \author cwike@keesaco.com of Keesaco
def open(	file_name,
			mode = 'r',
			MIME_type = None,
			options = None,
			read_buff_size = gcs.storage_api.ReadBuffer.DEFAULT_BUFFER_SIZE,
			retry_params = None	):
	try:
		file_handle = gcs.open( file_name, mode, MIME_type, options, read_buff_size, retry_params)
	
	except ValueError:
		return None
	else:
		return file_handle
	
	
## delete - deletes a resource
# \param cls - class reference
# \param file_name - name of resource to delete
# \param retry_params - (= None)
# \return boolean (true = success, false otherwise)
# \author jmccrea@keesaco.com of Keesaco
# \author cwike@keesaco.com of Keesaco
def delete(	file_name,
			retry_params = None	):
	try:
		gcs.delete(file_name, retry_params)
	except NotFoundError:
		return False
	else:
		return True
		

## stat - gets information about a specified resource
# \param cls - class reference
# \param file_name - name of resource to get information about
# \param retry_params - (= None)
# \return FileStat object - object containing information about specified resource, None on failure
# \author jmccrea@keesaco.com of Keesaco
# \author cwike@keesaco.com of Keesaco
def stat(	file_name,
			retry_params = None	):
	try:
		file_stat = gcs.stat( file_name )
	except NotFoundError:
		return None
	except AuthorizationError:
		return None
	else:
		return file_stat
	
	
## list_bucket - lists the contents of a storage bucket
# \param cls - class reference
# \param path - path of bucket to list (string)
# \param marker - (= None) further path, only resources following this marker will be listed
# \param prefix - (= None) DEPRECATED (Use path prefix)
# \param max_keys - (= None) limits the number of resources listed (None = no limit)
# \param delimiter - (= None) used to turn on directory mode (string of one or multiple characters used as a directory seperator)
# \param retry_params - (= None)
# \return list of FileStat objects
# \author jmccrea@keesaco.com of Keesaco
# \author cwike@keesaco.com of Keesaco
def list_bucket(	path,
					marker = None,
					prefix = None, ##deprecated
					max_keys = None,
					delimiter = None,
					retry_params = None	):
	file_stat_list =[]
	file_stat_iterator = gcs.listbucket( path, marker, prefix, max_keys, delimiter, retry_params)
	
	for file_stat in file_stat_iterator:
		file_stat_list.append(file_stat)
		
	return file_stat_list