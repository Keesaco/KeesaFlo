###########################################################################
## \file app/upload_handling.py
## \brief Custom upload handler that uses our Datastore API. Subclasses Django's FileUploadHandler.
## \author rmurley@keesaco.com of Keesaco
###########################################################################
## \package app.upload_handling
## \brief Custom upload handler that uses our Datastore API. Subclasses Django's FileUploadHandler.
###########################################################################
from django.core.files.uploadhandler import FileUploadHandler
import API.APIDatastore as ds

# Custom upload handler class.
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
        self.path = ds.generate_path('/fc-raw-data/', None, file_name)
        self.file_handle = ds.add_file(self.path, 'raw_data', 'w')
        print 'New file upload starting: %s (%s) [%s]' % (file_name, content_type, content_length)
        return None

    ###########################################################################
    ## \brief Called when the upload handler receives a 'chunk' of data. Writes this chunk to the file opened by new_file.
    ## \param raw_data - byte string containing the uploaded chunk
    ## \param start - position where the raw_data chunk begins
    ## \author rmurley@keesaco.com of Keesaco
    ###########################################################################
    def receive_data_chunk(self, raw_data, start):
        print 'Chunk get!'
        self.file_handle.write(raw_data)
        return None

    ###########################################################################
    ## \brief Called when a file has finished uploading. Simply closes the Datastore file.
    ## \param file_size - size of the uploaded file
    ## \author rmurley@keesaco.com of Keesaco
    ###########################################################################
    def file_complete(self, file_size):
        self.file_handle.close()
        print 'File upload complete!'
        return None