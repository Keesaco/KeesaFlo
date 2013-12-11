# Custom upload handler class.
from django.core.files.uploadhandler import FileUploadHandler
#import APIdatastore

# Custom upload handler class.
class fcsUploadHandler(FileUploadHandler):
    def __init__(self):
        FileUploadHandler.__init__(self)
        #add_directory('/raw_data')
        #self.path = generate_path('default/', 'raw_data', file_name) # SHOULD NOT BE NEEDED!

    # Called when a new file upload is starting, before upload handlers get any data.
    def new_file(self, field_name, file_name, content_type, content_length, charset):
        #self.path = generate_path('/', 'raw_data', file_name)
        #add_file(self.path)
        print 'New file upload starting: %s (%s) [%s]' % (file_name, content_type, content_length)
        return None

    # Receives a "chunk" of data from file upload.
    def receive_data_chunk(self, raw_data, start):
        #append(self.path, raw_data)
        print 'Chunk get!'
        return None

    # Called when the file has finished uploading.
    # Should return an UploadedFile object that will be stored in request.FILES.
    # Tricky one so currently just returning NONE.
    def file_complete(self, file_size):
        print 'File upload complete!'
        return None

    # Change chunk size experiment.
    def chunk_size():
        return 2**31