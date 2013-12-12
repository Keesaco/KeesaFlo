# Custom upload handler class.
from django.core.files.uploadhandler import FileUploadHandler
import API.APIDatastore as ds

# Custom upload handler class.
class fcsUploadHandler(FileUploadHandler):
    def __init__(self):
        FileUploadHandler.__init__(self)

    # Called when a new file upload is starting, before upload handlers get any data.
    def new_file(self, field_name, file_name, content_type, content_length, charset):
        self.path = ds.generate_path('/fc-raw-data/', None, file_name)
        self.file_handle = ds.add_file(self.path, 'raw_data', 'w')
        print 'New file upload starting: %s (%s) [%s]' % (file_name, content_type, content_length)
        return None

    # Receives a "chunk" of data from file upload.
    def receive_data_chunk(self, raw_data, start):
        self.file_handle.write(raw_data)
        print 'Chunk get!'
        return None

    # Called when the file has finished uploading.
    # Should return an UploadedFile object that will be stored in request.FILES.
    # Tricky one so currently just returning NONE.
    def file_complete(self, file_size):
        self.file_handle.close()
        print 'File upload complete!'
        return None