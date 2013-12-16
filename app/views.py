from django.http import HttpResponse
from django.shortcuts import render
from django import forms
import forms
from django.core.files.uploadhandler import FileUploadHandler
import upload_handling
import API.APIDatastore as ds;

def index(request):
	return render(request, 'index.html')

def about(request):
	return render(request, 'about.html')

def faq(request):
	return render(request, 'faq.html')

def app(request, file=None):
    lst = ds.list('/fc-raw-data')
    file_info = None
    for temp_file in lst: 
        temp_file.filename = temp_file.filename.rpartition('/')[2]
        if temp_file.filename == file :  file_info = temp_file
    return render(request, 'app.html', { 'files' : lst , 'file' : file_info})#{'files' : [{'filename' : 'hello', 'st_size' : '12' }]})#ds.list('/') })

def settings(request):
	return render(request, 'settings.html')

# Testing code for data upload
def upload(request):
    request.upload_handlers = [upload_handling.fcsUploadHandler()]
    if request.method == 'POST':
        form = forms.UploadFile(request.POST, request.FILES)
        #print request.FILES
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponse('File uploaded to %s' % request.FILES['file'].path)
        else:
            return render(request, 'upload.html', {'form': form})
    else:
        form = forms.UploadFile()
        return render(request, 'upload.html', {'form': form})
