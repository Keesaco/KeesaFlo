# Custom upload handler class.
from django.core.files.uploadhandler import FileUploadHandler
import API.APIDatastore as ds

# Custom upload handler class.
class fcsUploadHandler(FileUploadHandler):
    def __init__(self):
        FileUploadHandler.__init__(self)

    # Called when a new file upload is starting, before upload handlers get any data.
    def new_file(self, field_name, file_name, content_type, content_length, charset):
        self.path = ds.generate_path('/fc-raw-data/', 'raw_data', file_name)
        print 'New file upload starting: %s (%s) [%s]' % (file_name, content_type, content_length)
        return None

    # Receives a "chunk" of data from file upload.
    def receive_data_chunk(self, raw_data, start):
        ds.add_file(self.path, raw_data, 'w')
        print 'Chunk get!'
        return None

    # Called when the file has finished uploading.
    # Should return an UploadedFile object that will be stored in request.FILES.
    # Tricky one so currently just returning NONE.
    def file_complete(self, file_size):
        print 'File upload complete!'
        return None

    # Change the size of chunks buffered in memory.
    def chunk_size():
        return 2**31